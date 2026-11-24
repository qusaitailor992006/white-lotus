/**
 * ==============================================================================
 * WHITE LOTUS: FOOD VIBE FOLKS — TABLE RESERVATION WEBHOOK
 * Saras Baug Road, near Vyankatesh Apt, Parvati Paytha, Pune 411009
 * Table Desk: +91 95135 75757 | Open Daily: 12:00 PM – 11:30 PM
 * ==============================================================================
 * 
 * 3-MINUTE DEPLOYMENT INSTRUCTIONS:
 * 1. Open Google Sheets (https://sheets.new) and title the spreadsheet:
 *    "White Lotus Pune - Live Table Reservations"
 * 2. In the top menu, click: Extensions > Apps Script
 * 3. Delete any default code in Code.gs, paste this ENTIRE file, and click Save (💾).
 * 4. (Optional) Run `testSetup()` once to initialize headers.
 * 5. Click "Deploy" > "New deployment"
 * 6. Click the gear icon (⚙️) next to "Select type" and choose "Web app".
 * 7. Configure settings:
 *    - Description: "White Lotus Live Table Booking Webhook"
 *    - Execute as: "Me (your-email@gmail.com)"
 *    - Who has access: "Anyone"  <-- CRITICAL for frontend fetch requests
 * 8. Click "Deploy" and authorize permissions.
 * 9. Copy the generated Web app URL and paste into `index.html` at `GOOGLE_SHEETS_WEBHOOK_URL`.
 * ==============================================================================
 */

const SHEET_NAME = 'Reservations';
const NOTIFICATION_EMAIL = ''; // Optional: Enter manager email to receive instant alerts

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.tryLock(10000);

  try {
    let data;

    if (e && e.postData && e.postData.contents) {
      try {
        data = JSON.parse(e.postData.contents);
      } catch (jsonErr) {
        data = e.parameter || {};
      }
    } else if (e && e.parameter) {
      data = e.parameter;
    } else {
      data = {};
    }

    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let sheet = ss.getSheetByName(SHEET_NAME);

    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);
      initializeSheetHeaders(sheet);
    } else if (sheet.getLastRow() === 0) {
      initializeSheetHeaders(sheet);
    }

    const istTimestamp = Utilities.formatDate(new Date(), "Asia/Kolkata", "yyyy-MM-dd HH:mm:ss 'IST'");
    
    // Formula injection neutralization
    const refId = sanitizeSheetCell(data.refId || ('WL-' + new Date().getFullYear() + '-' + Math.random().toString(36).substring(2, 6).toUpperCase()));
    const guestName = sanitizeSheetCell(data.guestName || 'Guest Inquiry');
    const guestPhone = sanitizeSheetCell(data.guestPhone || 'Not Provided');
    const guestCount = sanitizeSheetCell(data.guestCount || '2 Guests');
    const reserveDate = sanitizeSheetCell(data.reserveDate || 'Today');
    const timeSlot = sanitizeSheetCell(data.timeSlot || 'Lunch');
    const seating = sanitizeSheetCell(data.seating || 'First Available');
    const specialRequests = sanitizeSheetCell(data.specialRequests || 'None');
    const source = sanitizeSheetCell(data.source || 'White Lotus Web Portal');
    const status = 'Confirmed / Pending Floor';

    sheet.appendRow([
      refId,
      istTimestamp,
      guestName,
      guestPhone,
      guestCount,
      reserveDate,
      timeSlot,
      seating,
      specialRequests,
      source,
      status
    ]);

    const lastRow = sheet.getLastRow();
    sheet.getRange(lastRow, 11).setBackground('#D1FAE5').setFontColor('#065F46').setFontWeight('bold');

    if (NOTIFICATION_EMAIL && NOTIFICATION_EMAIL.trim() !== '') {
      sendEmailAlert({
        refId: refId,
        timestamp: istTimestamp,
        name: guestName,
        phone: guestPhone,
        guests: guestCount,
        date: reserveDate,
        time: timeSlot,
        seating: seating,
        notes: specialRequests
      });
    }

    return ContentService.createTextOutput(JSON.stringify({
      status: 'success',
      message: 'Table reservation logged in White Lotus database',
      referenceId: refId
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: 'error',
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);

  } finally {
    lock.releaseLock();
  }
}

function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    status: 'online',
    restaurant: 'White Lotus: Food Vibe Folks',
    location: 'Saras Baug Road, Pune 411009',
    timings: 'Monday – Sunday, 12:00 PM – 11:30 PM',
    desk: '+91 95135 75757',
    timestamp: Utilities.formatDate(new Date(), "Asia/Kolkata", "yyyy-MM-dd HH:mm:ss 'IST'")
  })).setMimeType(ContentService.MimeType.JSON);
}

function initializeSheetHeaders(sheet) {
  const headers = [
    'Reference ID',
    'Timestamp (IST)',
    'Guest Name',
    'Phone / WhatsApp',
    'Party Size',
    'Visit Date',
    'Time Window',
    'Seating Preference',
    'Special Notes / Occasion',
    'Source',
    'Status'
  ];

  sheet.appendRow(headers);

  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange
    .setBackground('#0F241D')
    .setFontColor('#FFFFFF')
    .setFontWeight('bold')
    .setFontSize(10)
    .setHorizontalAlignment('center')
    .setVerticalAlignment('middle');

  sheet.setRowHeight(1, 35);
  sheet.setFrozenRows(1);

  sheet.setColumnWidth(1, 150); // Ref ID
  sheet.setColumnWidth(2, 170); // Timestamp
  sheet.setColumnWidth(3, 190); // Name
  sheet.setColumnWidth(4, 150); // Phone
  sheet.setColumnWidth(5, 140); // Guests
  sheet.setColumnWidth(6, 130); // Date
  sheet.setColumnWidth(7, 200); // Time Slot
  sheet.setColumnWidth(8, 190); // Seating
  sheet.setColumnWidth(9, 250); // Notes
  sheet.setColumnWidth(10, 140); // Source
  sheet.setColumnWidth(11, 160); // Status
}

function sanitizeSheetCell(val) {
  if (val === null || val === undefined) return '';
  let str = String(val).trim();
  if (/^[=\+\-\@\t\r]/.test(str)) {
    str = "'" + str;
  }
  return str;
}

function sendEmailAlert(booking) {
  try {
    const subject = `[White Lotus Booking] New Table: ${booking.name} (${booking.guests} on ${booking.date})`;
    const htmlBody = `
      <div style="font-family: Arial, sans-serif; background-color: #FAF8F5; padding: 24px; color: #111615;">
        <div style="max-width: 600px; margin: 0 auto; background: #FFFFFF; border: 1px solid #C5A059; border-radius: 8px; overflow: hidden;">
          <div style="background-color: #0F241D; padding: 18px 24px; color: #FAF8F5;">
            <h2 style="margin: 0; font-size: 18px; color: #DFBF7C; letter-spacing: 1px;">WHITE LOTUS: FOOD VIBE FOLKS</h2>
            <p style="margin: 4px 0 0; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: #C5A059;">Live Table Booking Notification • Saras Baug Rd, Pune</p>
          </div>
          
          <div style="padding: 24px;">
            <p style="font-size: 14px; margin-top: 0;">A new dining reservation has been requested via the web portal:</p>
            
            <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin: 16px 0;">
              <tr><td style="padding: 8px; border-bottom: 1px solid #F3EFE6; font-weight: bold; width: 35%;">Booking Ref:</td><td style="padding: 8px; border-bottom: 1px solid #F3EFE6;">${booking.refId}</td></tr>
              <tr><td style="padding: 8px; border-bottom: 1px solid #F3EFE6; font-weight: bold;">Guest Name:</td><td style="padding: 8px; border-bottom: 1px solid #F3EFE6;">${booking.name}</td></tr>
              <tr><td style="padding: 8px; border-bottom: 1px solid #F3EFE6; font-weight: bold;">Contact Phone:</td><td style="padding: 8px; border-bottom: 1px solid #F3EFE6;"><a href="tel:${booking.phone}">${booking.phone}</a></td></tr>
              <tr><td style="padding: 8px; border-bottom: 1px solid #F3EFE6; font-weight: bold;">Party Size:</td><td style="padding: 8px; border-bottom: 1px solid #F3EFE6;">${booking.guests}</td></tr>
              <tr><td style="padding: 8px; border-bottom: 1px solid #F3EFE6; font-weight: bold;">Date &amp; Time:</td><td style="padding: 8px; border-bottom: 1px solid #F3EFE6;">${booking.date} (${booking.time})</td></tr>
              <tr><td style="padding: 8px; border-bottom: 1px solid #F3EFE6; font-weight: bold;">Seating Area:</td><td style="padding: 8px; border-bottom: 1px solid #F3EFE6;">${booking.seating}</td></tr>
              <tr><td style="padding: 8px; border-bottom: 1px solid #F3EFE6; font-weight: bold;">Special Notes:</td><td style="padding: 8px; border-bottom: 1px solid #F3EFE6;">${booking.notes}</td></tr>
            </table>

            <div style="margin-top: 20px; padding: 12px; background: #F3EFE6; border-radius: 4px; font-size: 12px; color: #0F241D;">
              <strong>Action Required:</strong> Floor captain to allocate table and confirm seating via WhatsApp or direct phone call.
            </div>
          </div>
          
          <div style="background-color: #111615; padding: 12px 24px; font-size: 11px; color: #DFBF7C; text-align: center;">
            White Lotus: Food Vibe Folks • 202, 203 Saras Baug Rd, Pune • Desk: +91 95135 75757
          </div>
        </div>
      </div>
    `;

    MailApp.sendEmail({
      to: NOTIFICATION_EMAIL,
      subject: subject,
      htmlBody: htmlBody
    });
  } catch (err) {
    console.warn('Email dispatch warning:', err);
  }
}

function testSetup() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
  }
  initializeSheetHeaders(sheet);
  Logger.log("White Lotus table reservations sheet initialized.");
}
