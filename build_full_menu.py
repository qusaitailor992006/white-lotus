import json
import re

# Comprehensive dataset extracted directly from the 15 official White Lotus menu photos
menu_data = [
    # --- APPETIZERS NON-VEG ---
    {
        "category": "appetizers",
        "name": "Arabic Chicken",
        "type": "nonveg",
        "price": "₹432",
        "desc": "Grilled chicken shreds laced with za'atar and sumac served with hummus and pita chips.",
        "badge": "Middle Eastern"
    },
    {
        "category": "appetizers",
        "name": "Filipino Chicken Adobo",
        "type": "nonveg",
        "price": "₹432",
        "desc": "Chicken potato carrot bay leaf garlic ginger dark soy and vinegar.",
        "badge": "Global Specialty"
    },
    {
        "category": "appetizers",
        "name": "Tortang Talang",
        "type": "nonveg",
        "price": "₹384",
        "desc": "Smoked eggplant egg washed drizzled with kewpie mayo and togarashi spice.",
        "badge": "Chef Special"
    },
    {
        "category": "appetizers",
        "name": "Kimchi Chicken",
        "type": "nonveg",
        "price": "₹432",
        "desc": "Chicken sriracha sauce sesame oil black sesame Chinese cabbage rice vinegar.",
        "badge": "Korean Fusion"
    },
    {
        "category": "appetizers",
        "name": "Honey Chicken",
        "type": "nonveg",
        "price": "₹432",
        "desc": "Spicy chicken chili crisps chili oil and honey drizzle.",
        "badge": "Sweet & Spicy"
    },
    {
        "category": "appetizers",
        "name": "Korean Lamb",
        "type": "nonveg",
        "price": "₹534",
        "desc": "Roast lamb slices stir fried in spicy Korean sauce topped with pickled bell peppers.",
        "badge": "Tender Lamb"
    },
    {
        "category": "appetizers",
        "name": "Surmai Paturi",
        "type": "nonveg",
        "price": "₹572",
        "desc": "Kingfish marinated in grain mustard, wrapped in banana leaf and cooked on slow heat.",
        "badge": "Coastal Bengal"
    },
    {
        "category": "appetizers",
        "name": "Tandoori Pomfret",
        "type": "nonveg",
        "price": "₹826",
        "desc": "Tender whole pomfret cooked over tandoor served with kimchi salad.",
        "badge": "Clay Oven Seafood"
    },
    {
        "category": "appetizers",
        "name": "Fish Pahadi Tikka",
        "type": "nonveg",
        "price": "₹636",
        "desc": "Kingfish chunks marinated in mint and coriander paste tandoor cooked served with mint chutney.",
        "badge": "Kingfish Special"
    },
    {
        "category": "appetizers",
        "name": "Fish Lasooni Tikka",
        "type": "nonveg",
        "price": "₹648",
        "desc": "Kingfish chunks in garlic laced marinade cooked in tandoor served with toum.",
        "badge": "Garlic Glazed"
    },
    {
        "category": "appetizers",
        "name": "Tandoori Chicken",
        "type": "nonveg",
        "price": "₹425 / ₹633",
        "desc": "Whole baby chicken in red marinade cooked over tandoor served with onion salad (Half / Full).",
        "badge": "Tandoor Legend"
    },
    {
        "category": "appetizers",
        "name": "Chicken Raan",
        "type": "nonveg",
        "price": "₹658",
        "desc": "Whole Chicken marinated in house spice cooked to perfection.",
        "badge": "House Signature"
    },
    {
        "category": "appetizers",
        "name": "Double Cheese Kebab",
        "type": "nonveg",
        "price": "₹510",
        "desc": "Chicken Tangdi kebab with cheese filling and melted cheese topping.",
        "badge": "Melted Cheese"
    },
    {
        "category": "appetizers",
        "name": "Chicken Masala Tikka",
        "type": "nonveg",
        "price": "₹457",
        "desc": "Chicken tikka tossed in Indian spices tempered with ghee and curry leaves.",
        "badge": "Desi Ghee Tempered"
    },
    {
        "category": "appetizers",
        "name": "Malai Cheese Tikka",
        "type": "nonveg",
        "price": "₹470",
        "desc": "Chicken marinated in cream and cashew paste cooked over tandoor topped with cheese.",
        "badge": "Rich & Creamy"
    },
    {
        "category": "appetizers",
        "name": "Chicken Lasooni Kebab",
        "type": "nonveg",
        "price": "₹457",
        "desc": "Chicken in garlic marinade topped with burnt garlic served with mint chutney.",
        "badge": "Burnt Garlic"
    },
    {
        "category": "appetizers",
        "name": "Za'atari Chicken Kebab",
        "type": "nonveg",
        "price": "₹483",
        "desc": "Hammered chicken breast marinated in za'atar rolled and cooked over tandoor.",
        "badge": "Middle Eastern"
    },
    {
        "category": "appetizers",
        "name": "Murgh Sikandari Kebab",
        "type": "nonveg",
        "price": "₹483",
        "desc": "Triple Spicy Kebab with yellow chilli, green chili & bird eye chili served with mild cucumber dip.",
        "badge": "Triple Chili Heat"
    },
    {
        "category": "appetizers",
        "name": "Andhra Chicken Seekh",
        "type": "nonveg",
        "price": "₹457",
        "desc": "Minced Chicken, fresh coriander, garlic & mint served with brown onion hummus.",
        "badge": "Seekh Kebab"
    },
    {
        "category": "appetizers",
        "name": "Mutton Peshawari Kebab",
        "type": "nonveg",
        "price": "₹534",
        "desc": "Mutton tenderloin marinated in fried onion and mixed spices cooked over tandoor.",
        "badge": "Mutton Tenderloin"
    },
    {
        "category": "appetizers",
        "name": "Mutton Loncha",
        "type": "nonveg",
        "price": "₹534",
        "desc": "A fiery Kolhapuri delicacy of tender boneless mutton, slow-cooked with aromatic spices, roasted sesame, and dry coconut. Rustic taste of Maharashtra.",
        "badge": "Kolhapuri Heritage"
    },
    # MEAT ON STICK
    {
        "category": "appetizers",
        "name": "Thai Stick (Meat on Stick)",
        "type": "nonveg",
        "price": "₹482 / ₹608 / ₹508",
        "desc": "Authentic Thai marinated skewers grilled over charcoal, available in Veg / Chicken / Seafood.",
        "badge": "Meat On Stick"
    },
    {
        "category": "appetizers",
        "name": "Shish Taouk (Meat on Stick)",
        "type": "nonveg",
        "price": "₹708 / ₹515",
        "desc": "Lebanese char-grilled skewers served on wooden sticks with toum garlic dip and pickled vegetables.",
        "badge": "Meat On Stick"
    },

    # --- APPETIZERS VEG ---
    {
        "category": "appetizers",
        "name": "Kamal Ke Kabab",
        "type": "veg",
        "price": "₹384",
        "desc": "Lotus stem, chana dal, onion, green chilli and fresh coriander served with mint chutney.",
        "badge": "White Lotus Icon"
    },
    {
        "category": "appetizers",
        "name": "Dahi Ke Kabab",
        "type": "veg",
        "price": "₹367",
        "desc": "Indian fried tikki with hung curd and spices served with date and raisin relish.",
        "badge": "Crisp Exterior"
    },
    {
        "category": "appetizers",
        "name": "Mushroom Walnut Tikki",
        "type": "veg",
        "price": "₹372",
        "desc": "Sauteed button mushroom spiced with Indian spices mixed with roasted walnut crumbed and fried, served with Cajun mayo.",
        "badge": "Walnut Crumbed"
    },
    {
        "category": "appetizers",
        "name": "Malai Broccoli Kabab",
        "type": "veg",
        "price": "₹360",
        "desc": "Broccoli florets laced with cashew and almond marinade cooked over tandoor served with mint chutney.",
        "badge": "Tandoori Broccoli"
    },
    {
        "category": "appetizers",
        "name": "Chaap Banjara",
        "type": "veg",
        "price": "₹360",
        "desc": "Soya chaap laced with banjara marinade cooked over tandoor and finished with melted butter and cream.",
        "badge": "Soya Chaap"
    },
    {
        "category": "appetizers",
        "name": "Achari Boti",
        "type": "veg",
        "price": "₹381",
        "desc": "Soya chaap laced with Indian pickle marinade cooked in clay oven.",
        "badge": "Pickled Clay Oven"
    },
    {
        "category": "appetizers",
        "name": "Badam Tikki",
        "type": "veg",
        "price": "₹355",
        "desc": "Almond, raw papaya and mild spices served with burnt garlic dip.",
        "badge": "Almond & Papaya"
    },
    {
        "category": "appetizers",
        "name": "Sapo Paneer",
        "type": "veg",
        "price": "₹381",
        "desc": "Fresh cottage cheese, broccoli, and crisp bok choy tossed in savory Sapo sauce.",
        "badge": "Pan-Asian Wok"
    },
    {
        "category": "appetizers",
        "name": "Salt & Paneer",
        "type": "veg",
        "price": "₹393",
        "desc": "Corn, curd, stir fried with bell peppers and black pepper.",
        "badge": "Pepper Tossed"
    },
    {
        "category": "appetizers",
        "name": "Tobanjan Corn",
        "type": "veg",
        "price": "₹393",
        "desc": "Crispy American corn, red bell pepper, bird eye chili and spicy bean sauce.",
        "badge": "Crunchy Corn"
    },
    {
        "category": "appetizers",
        "name": "Tofu Tangsuyuk",
        "type": "veg",
        "price": "₹381",
        "desc": "Fried Tofu glazed in traditional Korean sweet and sour sauce.",
        "badge": "Korean Sweet & Sour"
    },
    {
        "category": "appetizers",
        "name": "Sambal Baby Potatoes",
        "type": "veg",
        "price": "₹330",
        "desc": "Baby potatoes tossed with extra spicy Indonesian sambal sauce and aromatics.",
        "badge": "Fiery Sambal"
    },
    {
        "category": "appetizers",
        "name": "Curry Basil Mushroom",
        "type": "veg",
        "price": "₹384",
        "desc": "Trio of wild mushrooms stir fried in curry oil and fresh aromatic sweet basil.",
        "badge": "Herb Infused"
    },
    {
        "category": "appetizers",
        "name": "Quesadillas",
        "type": "veg",
        "price": "₹355 / ₹445 / ₹407",
        "desc": "Soft tortilla filled with cheese, bell peppers, and onion dry roasted, served with sour cream.",
        "badge": "Mexican"
    },
    {
        "category": "appetizers",
        "name": "Mezze Platter",
        "type": "veg",
        "price": "₹418",
        "desc": "Hummus, smoked red pepper dip, crisp falafel, feta, olives, veg sticks, figs and pistachios.",
        "badge": "Mediterranean Feast"
    },
    {
        "category": "appetizers",
        "name": "Nawabi Dhingri",
        "type": "veg",
        "price": "₹402",
        "desc": "Button mushroom kebab stuffed with cheese, bell pepper and black currant in lasooni marinade with peanut thecha.",
        "badge": "Stuffed Mushroom"
    },
    {
        "category": "appetizers",
        "name": "Achaar Aur Cheese Ka Paneer",
        "type": "veg",
        "price": "₹406",
        "desc": "Paneer sandwiched with a tangy spiced cheese and mango pickle stuffing.",
        "badge": "Stuffed Paneer"
    },
    {
        "category": "appetizers",
        "name": "Paneer Bara Kebab",
        "type": "veg",
        "price": "₹418",
        "desc": "Paneer cubes with black currant, dry chilli and walnuts laced with malai marinade served with mint chutney.",
        "badge": "Walnut & Malai"
    },
    {
        "category": "appetizers",
        "name": "Paneer Kaju Malai Roll",
        "type": "veg",
        "price": "₹432",
        "desc": "Paneer roll kebab stuffed with crushed dry fruits and served with garlic mayo.",
        "badge": "Royal Roll"
    },
    {
        "category": "appetizers",
        "name": "Paneer Lollipop",
        "type": "veg",
        "price": "₹418",
        "desc": "Paneer popsicle layered with cheese, mushroom and burnt garlic served with tamarind and mint chutney.",
        "badge": "Popsicle Skewer"
    },

    # --- SOUPS, SALADS, MUNCH ON & BAO ---
    {
        "category": "soups-salads-bao",
        "name": "Bell Pepper and Basil Soup",
        "type": "veg",
        "price": "₹262",
        "desc": "Fresh sweet basil pesto, roasted bell peppers and velvety cream.",
        "badge": "Warm Velouté"
    },
    {
        "category": "soups-salads-bao",
        "name": "Cream of Mushroom",
        "type": "veg",
        "price": "₹266",
        "desc": "Roasted mushroom puree, dried mushroom dust, fresh dairy cream, and cheese.",
        "badge": "Classic Potage"
    },
    {
        "category": "soups-salads-bao",
        "name": "Chicken Chowder Soup",
        "type": "nonveg",
        "price": "₹288 / ₹264",
        "desc": "Thick creamy country broth with potato, crushed sweet corn and cheese.",
        "badge": "Country Chowder"
    },
    {
        "category": "soups-salads-bao",
        "name": "Roasted Almond Soup",
        "type": "veg",
        "price": "₹238 / ₹306 / ₹278",
        "desc": "Silky almond paste, fresh wild oregano, and cream white soup.",
        "badge": "Almond Velouté"
    },
    {
        "category": "soups-salads-bao",
        "name": "Tom Kha Soup",
        "type": "veg",
        "price": "₹266 / ₹306 / ₹279",
        "desc": "Button mushroom, babycorn, carrot, beans, bok choy, coconut milk, lemongrass, galangal, kaffir lime.",
        "badge": "Thai Coconut Broth"
    },
    {
        "category": "soups-salads-bao",
        "name": "Zaffrani Murgh Ka Shorba",
        "type": "nonveg",
        "price": "₹282",
        "desc": "Kashmiri saffron laced chicken and cream broth with whole mild aromatics.",
        "badge": "Saffron Shorba"
    },
    {
        "category": "soups-salads-bao",
        "name": "Lotus Salad",
        "type": "veg",
        "price": "₹381",
        "desc": "Lotus root, fresh pomegranate pearls, coriander, roasted sesame seeds, smoked pepper lemon dressing.",
        "badge": "Signature Salad"
    },
    {
        "category": "soups-salads-bao",
        "name": "Thai Mango Salad",
        "type": "veg",
        "price": "₹381",
        "desc": "Coriander, red & yellow bell peppers, red onion, raw mango, bird eye chilli, roasted crushed peanuts.",
        "badge": "Zesty & Crisp"
    },
    {
        "category": "soups-salads-bao",
        "name": "Crispy Chicken Salad",
        "type": "nonveg",
        "price": "₹496",
        "desc": "Crispy fried chicken morsels coated in honey balsamic mixed leaves & parmesan ranch dressing.",
        "badge": "Ranch & Balsamic"
    },
    {
        "category": "soups-salads-bao",
        "name": "Shish Fattoush Bin Labneh",
        "type": "nonveg",
        "price": "₹499",
        "desc": "Lebanese garlic chicken with cucumber, onions, lettuce and tomatoes tossed in yogurt dressing topped with pita crisps.",
        "badge": "Lebanese Bowl"
    },
    {
        "category": "soups-salads-bao",
        "name": "Loaded Fries",
        "type": "veg",
        "price": "₹317",
        "desc": "Panko crusted french fries drenched in melted cheese sauce dusted with sumac.",
        "badge": "Munch On"
    },
    {
        "category": "soups-salads-bao",
        "name": "Chatpata Cheese Cherry",
        "type": "veg",
        "price": "₹281",
        "desc": "Cheese cubes, maraschino cherries, pineapple skewers with chat masala.",
        "badge": "Retro Classic"
    },
    {
        "category": "soups-salads-bao",
        "name": "Bruschetta Pomodoro",
        "type": "veg",
        "price": "₹336",
        "desc": "Toasted baguette slices, black olives, vine ripe tomatoes, extra virgin olive oil, parmesan cheese.",
        "badge": "Antipasti"
    },
    {
        "category": "soups-salads-bao",
        "name": "Kung Pao Paneer Bao",
        "type": "veg",
        "price": "₹390",
        "desc": "Steamed fluffy open bao stuffed with fried paneer, soya chilli, tomato ketchup, red bell pepper, scallions & shaoxing sauce.",
        "badge": "Steamed Bao"
    },
    {
        "category": "soups-salads-bao",
        "name": "Chilli Chicken Bao",
        "type": "nonveg",
        "price": "₹406",
        "desc": "Deep fried chicken, tri-color peppers, chilli soya sauce served with creamy dynamite sauce.",
        "badge": "Dynamite Bao"
    },
    {
        "category": "soups-salads-bao",
        "name": "Spicy Mushroom Bao",
        "type": "veg",
        "price": "₹385",
        "desc": "Wood ear fungus, shiitake, and button mushrooms tossed in spicy peanut sauce in steamed bao.",
        "badge": "Mushroom Trio"
    },

    # --- PIZZA, PASTA & RISOTTO ---
    {
        "category": "pizza-pasta-risotto",
        "name": "Margarita Pizza",
        "type": "veg",
        "price": "₹445",
        "desc": "San Marzano plum tomato sauce, mozzarella, fresh basil, and oregano on stone-baked crust.",
        "badge": "Stone-Fired"
    },
    {
        "category": "pizza-pasta-risotto",
        "name": "White Mushroom Pizza",
        "type": "veg",
        "price": "₹445 / ₹509 / ₹483",
        "desc": "Cheese spread, caramelized balsamic onions, wilted tomato, sautéed mushrooms, and fresh sweet basil.",
        "badge": "Chef Special Pizza"
    },
    {
        "category": "pizza-pasta-risotto",
        "name": "Supreme Seafood Pizza",
        "type": "nonveg",
        "price": "₹509",
        "desc": "Kingfish, fresh Arabian prawns, squid rings, red onions, roasted peppers, and pickled gherkins.",
        "badge": "Seafood Feast"
    },
    {
        "category": "pizza-pasta-risotto",
        "name": "Chicago Mince Pizza",
        "type": "nonveg",
        "price": "₹483 / ₹509",
        "desc": "Deep crust topped with spiced pizza mince meat, buttery mashed potato, and mozzarella blend.",
        "badge": "Chicago Style"
    },
    {
        "category": "pizza-pasta-risotto",
        "name": "Florentine Chicken Pizza",
        "type": "nonveg",
        "price": "₹483",
        "desc": "Roast chicken, sun dried tomato, wilted baby spinach, cherry tomatoes, and mozzarella.",
        "badge": "Tuscan Crust"
    },
    {
        "category": "pizza-pasta-risotto",
        "name": "Baked Lasagne",
        "type": "veg",
        "price": "₹483 / ₹521",
        "desc": "Layered artisanal pasta sheets baked with creamy wild mushrooms, spinach, bechamel and mozzarella.",
        "badge": "Al Forno"
    },
    {
        "category": "pizza-pasta-risotto",
        "name": "Mushroom Ragu Penne",
        "type": "veg",
        "price": "₹483",
        "desc": "Shiitake mushroom, button mushroom, oyster mushroom, white wine cream, parmesan cheese penne.",
        "badge": "Wild Forest Ragu"
    },
    {
        "category": "pizza-pasta-risotto",
        "name": "Classic Alfredo Pasta",
        "type": "veg",
        "price": "₹483 / ₹584 / ₹509",
        "desc": "Velvety white sauce, white wine, country butter, cream cheese, parmesan penne (Veg / Chicken / Seafood).",
        "badge": "Rich Cream"
    },
    {
        "category": "pizza-pasta-risotto",
        "name": "Pomodoro Penne",
        "type": "veg",
        "price": "₹584 / ₹509",
        "desc": "Vine tomato sauce, sun dried zucchini, yellow squash, cherry tomatoes, port wine penne.",
        "badge": "Port Wine Infused"
    },
    {
        "category": "pizza-pasta-risotto",
        "name": "Chicken Bolognese Spaghetti",
        "type": "nonveg",
        "price": "₹509",
        "desc": "Slow-simmered minced chicken, fresh basil brown sauce, tomato sauce, red wine and parmesan over spaghetti.",
        "badge": "Red Wine Bolognese"
    },
    {
        "category": "pizza-pasta-risotto",
        "name": "Risotto Pomodoro",
        "type": "veg",
        "price": "₹546",
        "desc": "Italian arborio rice cooked in white wine and veg stock, sundried tomato, pomodoro sauce, cream and parmesan.",
        "badge": "Arborio Risotto"
    },
    {
        "category": "pizza-pasta-risotto",
        "name": "Risotto Fungi",
        "type": "veg",
        "price": "₹572",
        "desc": "Button mushroom, mascarpone cheese, arborio rice and roasted wild mushroom dust.",
        "badge": "Porcini Dust"
    },
    {
        "category": "pizza-pasta-risotto",
        "name": "Risotto Seafood",
        "type": "nonveg",
        "price": "₹763",
        "desc": "Prawns, squid, kingfish, white wine broth, parmesan cheese and slow-stirred arborio rice.",
        "badge": "Coastal Risotto"
    },
    {
        "category": "pizza-pasta-risotto",
        "name": "Risotto Pollo",
        "type": "nonveg",
        "price": "₹658",
        "desc": "Roast chicken, mascarpone cheese, arborio rice cooked with herbs and cream.",
        "badge": "Pollo Cremoso"
    },

    # --- BOWLS & CONTINENTAL MAINS ---
    {
        "category": "bowls-continental",
        "name": "Burmese Khow Suey Bowl",
        "type": "veg",
        "price": "₹509 / ₹711 / ₹572",
        "desc": "Khow Suey bowl with burnt garlic noodles, boiled egg, fried onion, crushed peanut & rich spiced coconut curry broth (Veg / Prawn / Chicken).",
        "badge": "#1 Diner Star"
    },
    {
        "category": "bowls-continental",
        "name": "Thai Green Curry Bowl",
        "type": "veg",
        "price": "₹534 / ₹713 / ₹558",
        "desc": "Aromatic green curry with fresh basil rice, steamed red cabbage, bamboo shoots and roasted peanuts.",
        "badge": "Bangkok Bowl"
    },
    {
        "category": "bowls-continental",
        "name": "Korean Rice Bowl",
        "type": "veg",
        "price": "₹509 / ₹687 / ₹535",
        "desc": "Fermented black bean, red chili, red bell pepper, ginger, scallions, sautéed kale, and steamed rice.",
        "badge": "Seoul Flavors"
    },
    {
        "category": "bowls-continental",
        "name": "Panang Curry Bowl",
        "type": "veg",
        "price": "₹534 / ₹687",
        "desc": "Sweet and spicy rich Panang curry served with steamed jasmine rice and red cabbage slaw.",
        "badge": "Panang Curry"
    },
    {
        "category": "bowls-continental",
        "name": "Pollo Ajode Majo",
        "type": "nonveg",
        "price": "₹614",
        "desc": "Grilled chicken breast topped with cheese and tomatoes baked, finished with Mexican barbecue sauce, tomato rice and sautéed vegetables.",
        "badge": "Mexican Grill"
    },
    {
        "category": "bowls-continental",
        "name": "Farouj Musahab",
        "type": "nonveg",
        "price": "₹608",
        "desc": "Lebanese boneless roast chicken served with tahini sauce, hummus, sautéed vegetables and fragrant saffron rice.",
        "badge": "Beirut Platter"
    },
    {
        "category": "bowls-continental",
        "name": "Smoked Chicken Roulade",
        "type": "nonveg",
        "price": "₹602",
        "desc": "Herbed chicken roulade, smoked and served with fig jus, sautéed garden vegetables and roasted baby potato.",
        "badge": "Fig Jus Reduction"
    },
    {
        "category": "bowls-continental",
        "name": "Chicken Steak",
        "type": "nonveg",
        "price": "₹608",
        "desc": "Tender chicken steak served with herbed rice, sautéed vegetables, potato mash and red wine pepper sauce.",
        "badge": "Pepper Steak"
    },
    {
        "category": "bowls-continental",
        "name": "Lamb Steak",
        "type": "nonveg",
        "price": "₹763",
        "desc": "Prime lamb undercut, roasted garlic jus, grilled Malta orange, sautéed vegetables, and roasted baby potatoes.",
        "badge": "Undercut Lamb"
    },
    {
        "category": "bowls-continental",
        "name": "Grilled Fish Fillet",
        "type": "nonveg",
        "price": "₹763",
        "desc": "Kingfish fillet, French Bercy sauce, creamy cheese mash potato, sautéed kale and cherry tomato salad.",
        "badge": "Kingfish Fillet"
    },
    {
        "category": "bowls-continental",
        "name": "Chicken Cordon Bleu",
        "type": "nonveg",
        "price": "₹622",
        "desc": "Crumb-crusted chicken stuffed with cheese, served with balsamic glazed green beans and garlic mashed cauliflower.",
        "badge": "French Classic"
    },

    # --- MAIN COURSE (VEG & NON-VEG) ---
    {
        "category": "mains",
        "name": "Old Delhi Butter Chicken",
        "type": "nonveg",
        "price": "₹509",
        "desc": "Tandoor chicken chunks loaded with rich dairy cream and churned butter in velvety vine tomato gravy.",
        "badge": "Old Delhi Royalty"
    },
    {
        "category": "mains",
        "name": "Dhaba Chicken Curry",
        "type": "nonveg",
        "price": "₹467",
        "desc": "Simple, rustic and deliciously made countryside chicken curry with roasted ground spices.",
        "badge": "Rustic Kadhai"
    },
    {
        "category": "mains",
        "name": "Murgh E Khas",
        "type": "nonveg",
        "price": "₹458",
        "desc": "Whole chicken leg grilled, simmered in rich cashew paste, brown onion gravy and royal garam masala.",
        "badge": "Chef Special"
    },
    {
        "category": "mains",
        "name": "Murgh Tikka Lababdar",
        "type": "nonveg",
        "price": "₹483",
        "desc": "Tandoor-charred chicken tikka cubes in a luscious tomato-onion lababdar gravy with fresh cream.",
        "badge": "Lababdar Gravy"
    },
    {
        "category": "mains",
        "name": "Murgh Kadhai",
        "type": "nonveg",
        "price": "₹458",
        "desc": "Chicken tossed in cast iron kadhai with crushed coriander seeds, bell peppers, and onion gravy.",
        "badge": "Kadhai Spices"
    },
    {
        "category": "mains",
        "name": "Chicken Malwani",
        "type": "nonveg",
        "price": "₹469",
        "desc": "Konkan coast style medium spicy chicken curry flavored with fresh coconut and triphala.",
        "badge": "Konkan Coast"
    },
    {
        "category": "mains",
        "name": "Murgh Sukha",
        "type": "nonveg",
        "price": "₹458",
        "desc": "Dry chicken preparation tossed with whole spices, roasted dry coconut, and lasoon chutney.",
        "badge": "Dry Roast"
    },
    {
        "category": "mains",
        "name": "Slow-Braised Rahra Gosht",
        "type": "nonveg",
        "price": "₹661",
        "desc": "Tender bone-in mutton pieces cooked alongside seasoned mutton keema mince in thick red gravy.",
        "badge": "Mutton Royale"
    },
    {
        "category": "mains",
        "name": "Champaran Mutton",
        "type": "nonveg",
        "price": "₹661",
        "desc": "Slow-cooked in earthen handi sealed with dough, mustard oil, desi ghee, garlic pods, ginger and whole spices.",
        "badge": "Handi Ahuna Mutton"
    },
    {
        "category": "mains",
        "name": "Mutton Bhuna",
        "type": "nonveg",
        "price": "₹661",
        "desc": "Tender mutton slow roasted in its own juices with thick caramelized onion and tomato masala.",
        "badge": "Bhuna Masala"
    },
    {
        "category": "mains",
        "name": "Mutton Kheema Pav",
        "type": "nonveg",
        "price": "₹420",
        "desc": "Spiced minced mutton cooked in local Pune/Mumbai style, served piping hot with buttered laadi pav.",
        "badge": "Street to Table"
    },
    {
        "category": "mains",
        "name": "Malabari Fish Curry",
        "type": "nonveg",
        "price": "₹636",
        "desc": "Surmai kingfish simmered in dry red chili and coconut milk gravy tempered with fresh curry leaves and coconut oil.",
        "badge": "Malabar Coast"
    },
    {
        "category": "mains",
        "name": "Jhinga Hara Masala",
        "type": "nonveg",
        "price": "₹636",
        "desc": "Arabian Sea prawns tossed in fiery green chili thecha and spiced tomato onion masala.",
        "badge": "Kolhapuri Thecha"
    },
    {
        "category": "mains",
        "name": "Chingri Malai Curry",
        "type": "nonveg",
        "price": "₹650",
        "desc": "Prawns simmered in fragrant onion paste, coconut milk, mild red chili and golden turmeric.",
        "badge": "Bengali Malai"
    },
    # VEG MAINS
    {
        "category": "mains",
        "name": "Diwani Handi",
        "type": "veg",
        "price": "₹455",
        "desc": "Exotic garden vegetables, baby corn and spinach simmered in fragrant onion-saffron gravy.",
        "badge": "Saffron Gravy"
    },
    {
        "category": "mains",
        "name": "Paneer Lababdar",
        "type": "veg",
        "price": "₹445",
        "desc": "Fresh cottage cheese cubes folded in sweet and spicy tomato-onion cream gravy.",
        "badge": "North Indian Star"
    },
    {
        "category": "mains",
        "name": "Paneer Punjabi",
        "type": "veg",
        "price": "₹483",
        "desc": "Double paneer slices sandwiched with spicy mint chutney, cooked in onion gravy with cheese cream.",
        "badge": "Mint Sandwiched"
    },
    {
        "category": "mains",
        "name": "Malai Paneer Tikka Masala",
        "type": "veg",
        "price": "₹458",
        "desc": "Clay oven roasted malai paneer kebabs simmered in cashew paste, tomato gravy and butter.",
        "badge": "Cashew Makhani"
    },
    {
        "category": "mains",
        "name": "Sham Savera",
        "type": "veg",
        "price": "₹483",
        "desc": "Spinach and cottage cheese koftas topped with melted cheese, placed on rich creamy tomato velvet gravy.",
        "badge": "Master Kofta"
    },
    {
        "category": "mains",
        "name": "Hare Moti",
        "type": "veg",
        "price": "₹408",
        "desc": "Sweet green peas and cheese cubes simmered in a luscious spinach gravy and heavy cream.",
        "badge": "Palak & Paneer"
    },
    {
        "category": "mains",
        "name": "Mushroom Kali Mirch",
        "type": "veg",
        "price": "₹456",
        "desc": "Button mushrooms simmered in freshly crushed black pepper laced cashew and cream gravy.",
        "badge": "Tellicherry Pepper"
    },
    {
        "category": "mains",
        "name": "Rajbhog Kofta",
        "type": "veg",
        "price": "₹432",
        "desc": "Veg kofta layered with saffron paneer mix, crumb fried and simmered in creamy cashew and onion gravy.",
        "badge": "Saffron Kofta"
    },
    {
        "category": "mains",
        "name": "Aloo Dum Daar",
        "type": "veg",
        "price": "₹408",
        "desc": "Potato scooped and filled with minced vegetables, cooked over tandoor on saffron laced cashew and onion gravy.",
        "badge": "Tandoori Stuffed"
    },
    {
        "category": "mains",
        "name": "Dal Makhni",
        "type": "veg",
        "price": "₹406",
        "desc": "Black lentils slow-cooked overnight with vine tomatoes, fresh churned butter, and cream.",
        "badge": "Overnight Simmer"
    },
    {
        "category": "mains",
        "name": "Dal Tadka / Dal Palak",
        "type": "veg",
        "price": "₹279",
        "desc": "Yellow toor dal tempered with desi ghee, cumin, garlic, dry red chilies and fresh spinach.",
        "badge": "Desi Tadka"
    },

    # --- BREADS, RICE & NOODLES ---
    {
        "category": "breads-rice-noodles",
        "name": "Tandoori Roti (Plain / Butter)",
        "type": "veg",
        "price": "₹54 / ₹65",
        "desc": "Whole wheat flatbread baked fresh inside clay tandoor oven.",
        "badge": "Clay Oven"
    },
    {
        "category": "breads-rice-noodles",
        "name": "Naan (Plain / Butter)",
        "type": "veg",
        "price": "₹72 / ₹76",
        "desc": "Classic refined flour soft flatbread brushed with country butter.",
        "badge": "Clay Oven"
    },
    {
        "category": "breads-rice-noodles",
        "name": "Garlic Naan (Plain / Butter)",
        "type": "veg",
        "price": "₹104 / ₹114",
        "desc": "Tandoor naan generously topped with minced roasted garlic and coriander.",
        "badge": "Garlic Butter"
    },
    {
        "category": "breads-rice-noodles",
        "name": "Cheese Garlic Naan",
        "type": "veg",
        "price": "₹180 / ₹191",
        "desc": "Stuffed with melted cheese and topped with golden toasted garlic.",
        "badge": "Stuffed Cheese"
    },
    {
        "category": "breads-rice-noodles",
        "name": "Mutton Ghee Roast Biryani",
        "type": "nonveg",
        "price": "₹682",
        "desc": "Tender mutton pieces tossed in coastal Mangalorean ghee roast spices, layered with fragrant basmati dum rice.",
        "badge": "House Special Biryani"
    },
    {
        "category": "breads-rice-noodles",
        "name": "Dum Biryani (Veg / Chicken / Mutton)",
        "type": "nonveg",
        "price": "₹342 / ₹480 / ₹612",
        "desc": "Slow-cooked handi dum biryani with long grain basmati rice, mint, saffron milk and fried onions.",
        "badge": "Handi Dum"
    },
    {
        "category": "breads-rice-noodles",
        "name": "Hakka Noodles (Veg / Chicken / Prawn)",
        "type": "veg",
        "price": "₹318 / ₹648 / ₹406",
        "desc": "Thin noodles wok-tossed with julienned veggies, scallions, light soy and white pepper.",
        "badge": "Wok Tossed"
    },
    {
        "category": "breads-rice-noodles",
        "name": "Burnt Garlic Fried Rice",
        "type": "veg",
        "price": "₹305 / ₹635 / ₹378",
        "desc": "Jasmine rice tossed with crunchy golden burnt garlic flakes and scallions.",
        "badge": "Burnt Garlic"
    },
    {
        "category": "breads-rice-noodles",
        "name": "Nasi Goreng Rice",
        "type": "nonveg",
        "price": "₹308 / ₹637 / ₹410",
        "desc": "Indonesian wok rice with sweet soy, chili paste, scallions, topped with a fried sunny egg.",
        "badge": "Indonesian"
    },

    # --- DESSERTS & NATURAL ICE CREAMS ---
    {
        "category": "desserts-icecream",
        "name": "Tiramisu",
        "type": "veg",
        "price": "₹393",
        "desc": "Espresso drenched gingersnaps, airy Italian coffee zabaglione custard, and Belgian cocoa powder.",
        "badge": "Pune's #1 Dessert"
    },
    {
        "category": "desserts-icecream",
        "name": "Baked New York Cheese Cake",
        "type": "veg",
        "price": "₹406",
        "desc": "Dense Philadelphia cream cheese cake with salted caramel drizzle and bitter filter coffee ice cream.",
        "badge": "Filter Coffee Pairing"
    },
    {
        "category": "desserts-icecream",
        "name": "Red Velvet Cheese Cake",
        "type": "veg",
        "price": "₹406",
        "desc": "Velvety red cocoa sponge swirled with cheese mousse, brandy pralines, and crunchy Oreo mash.",
        "badge": "Brandy Pralines"
    },
    {
        "category": "desserts-icecream",
        "name": "Walnut Brownie Sizzler",
        "type": "veg",
        "price": "₹355",
        "desc": "Sizzling dark chocolate fudge brownie with caramelized grilled pineapple and pure vanilla ice cream.",
        "badge": "Sizzling Hot"
    },
    {
        "category": "desserts-icecream",
        "name": "Paan Firni",
        "type": "veg",
        "price": "₹270",
        "desc": "Traditional slow-churned basmati rice pudding infused with sweet Calcutta paan and gulkand.",
        "badge": "Calcutta Paan"
    },
    {
        "category": "desserts-icecream",
        "name": "Misti Doi",
        "type": "veg",
        "price": "₹198",
        "desc": "Traditional Bengali caramelized sweet creamy curd set and served in rustic earthen clay mud cups.",
        "badge": "Clay Cup"
    },
    {
        "category": "desserts-icecream",
        "name": "Gulkand Natural Ice Cream",
        "type": "veg",
        "price": "₹312",
        "desc": "A delicate blend of fragrant royal Damascus rose petal gulkand folded into dense cream.",
        "badge": "Authentic Natural"
    },
    {
        "category": "desserts-icecream",
        "name": "Gud And Sauf Natural Ice Cream",
        "type": "veg",
        "price": "₹291",
        "desc": "Rich, earthy natural sugarcane jaggery (gud) and sweet roasted fennel seeds (sauf) in pure churned milk.",
        "badge": "Deeply Indian"
    },
    {
        "category": "desserts-icecream",
        "name": "Apple Pie Natural Ice Cream",
        "type": "veg",
        "price": "₹330",
        "desc": "Sweet stewed apples, comforting cinnamon spice and buttery pie crust crumb in every spoonful.",
        "badge": "Spiced Apple"
    },
    {
        "category": "desserts-icecream",
        "name": "Cookie Dusk Natural Ice Cream",
        "type": "veg",
        "price": "₹303",
        "desc": "Buttery, crunchy Speculoos cookie chunks folded into sweet cream for ultimate comfort.",
        "badge": "Cookie Comfort"
    },
    {
        "category": "desserts-icecream",
        "name": "Midnight Mania Natural Ice Cream",
        "type": "veg",
        "price": "₹269",
        "desc": "Decadent dark Dutch cocoa chocolate ice cream made for serious late-night cravings.",
        "badge": "Dark Chocolate"
    },

    # --- THE BAR & MIXOLOGY DECK ---
    {
        "category": "bar-mixology",
        "name": "Classic Mojito (Alcoholic)",
        "type": "bar",
        "price": "₹589",
        "desc": "White rum, muddled fresh lime wedges, garden mint, cane syrup topped with effervescent soda.",
        "badge": "White Rum Cocktail"
    },
    {
        "category": "bar-mixology",
        "name": "Spicy Mango Mojito",
        "type": "bar",
        "price": "₹589",
        "desc": "White rum, Tabasco drops, fresh lime, garden mint, Alphonso mango crush and club soda.",
        "badge": "Tabasco & Mango"
    },
    {
        "category": "bar-mixology",
        "name": "Cucumber Basil Mojito",
        "type": "bar",
        "price": "₹589",
        "desc": "White rum, fresh lime, garden mint, Italian sweet basil, and cooling cucumber syrup.",
        "badge": "Refreshing Herb"
    },
    {
        "category": "bar-mixology",
        "name": "Virgin Mojito (Mocktail)",
        "type": "veg",
        "price": "₹360",
        "desc": "Fresh garden mint, crushed lime wedges, mint syrup, sweet 'n sour topped with chilled soda or Sprite.",
        "badge": "Zero-Proof Mocktail"
    },
    {
        "category": "bar-mixology",
        "name": "Lotus Fruit Punch",
        "type": "veg",
        "price": "₹340",
        "desc": "Apple juice, Alphonso mango juice, Valencia orange, pineapple juice, and house-made lotus cinnamon syrup.",
        "badge": "House Punch"
    },
    {
        "category": "bar-mixology",
        "name": "Masala Guava",
        "type": "veg",
        "price": "₹360",
        "desc": "Pink guava juice, fresh lime, Himalayan black salt, red chili rim, and a dash of Tabasco.",
        "badge": "Chili Rimmed"
    },
    {
        "category": "bar-mixology",
        "name": "Oreo Crunch Thick Shake",
        "type": "veg",
        "price": "₹299",
        "desc": "Crushed Oreo biscuits blended with chilled whole milk and heavy vanilla ice cream.",
        "badge": "Gourmet Shake"
    },
    {
        "category": "bar-mixology",
        "name": "Kit Kat Creamy Shake",
        "type": "veg",
        "price": "₹299",
        "desc": "Crisp Kit Kat wafer bars blended with dairy milk, chocolate ganache and ice cream.",
        "badge": "Gourmet Shake"
    },
    {
        "category": "bar-mixology",
        "name": "Apple Almond Shake",
        "type": "veg",
        "price": "₹299",
        "desc": "Sweet apples, California roasted almonds, cinnamon powder, vanilla bean, milk and ice cream.",
        "badge": "Almond Cinnamon"
    },
    {
        "category": "bar-mixology",
        "name": "Glenfiddich 12 Yr (Single Malt)",
        "type": "bar",
        "price": "₹830 / ₹1,650 / ₹19,700",
        "desc": "Distinctive Speyside single malt scotch, matured in American bourbon and Spanish sherry oak casks (30ml / 60ml / Bottle).",
        "badge": "Speyside Single Malt"
    },
    {
        "category": "bar-mixology",
        "name": "Indri Trini (Indian Single Malt)",
        "type": "bar",
        "price": "₹650 / ₹1,290 / ₹15,400",
        "desc": "Award-winning Indian single malt matured in three wooden barrels: ex-bourbon, ex-wine, and Pedro Ximenez sherry (30ml / 60ml / Bottle).",
        "badge": "Award Winning Malt"
    },
    {
        "category": "bar-mixology",
        "name": "Johnnie Walker Blue Label",
        "type": "bar",
        "price": "₹2,800 / ₹5,400 / ₹59,000",
        "desc": "The pinnacle of blended Scotch whisky crafted from rare hand-selected casks across Scotland (30ml / 60ml / Bottle).",
        "badge": "Ultra Luxury Scotch"
    },
    {
        "category": "bar-mixology",
        "name": "Johnnie Walker Black Label",
        "type": "bar",
        "price": "₹520 / ₹1,010 / ₹12,100",
        "desc": "12-year-old icon of master blending featuring rich smoky embers and sweet dark fruits (30ml / 60ml / Bottle).",
        "badge": "12 Yr Scotch"
    },
    {
        "category": "bar-mixology",
        "name": "Chivas Regal 12 Yr",
        "type": "bar",
        "price": "₹520 / ₹1,010 / ₹12,100",
        "desc": "Smooth blended Scotch whisky with notes of wild herbs, heather, honey, and orchard fruits (30ml / 60ml / Bottle).",
        "badge": "12 Yr Scotch"
    },
    {
        "category": "bar-mixology",
        "name": "Grey Goose Vodka",
        "type": "bar",
        "price": "₹640 / ₹1,260 / ₹15,120",
        "desc": "French master-crafted wheat vodka distilled from single-origin Picardie wheat and spring water (30ml / 60ml / Bottle).",
        "badge": "French Vodka"
    },
    {
        "category": "bar-mixology",
        "name": "Beluga Gold Line Vodka",
        "type": "bar",
        "price": "₹2,500 / ₹4,800 / ₹57,000",
        "desc": "Limited edition Siberian luxury vodka rested for 90 days with notes of rice and floral extracts (30ml / 60ml / Bottle).",
        "badge": "Ultra Premium Vodka"
    },
    {
        "category": "bar-mixology",
        "name": "Craft Shots (Jägerbomb / Duck Fat)",
        "type": "bar",
        "price": "₹450 – ₹680",
        "desc": "Duck Fat Shot (₹680), Jäger Bomb (₹680), Kamikaze Blue (₹450), Mexican Samurai (₹450), Tiramisu Shot (₹680), Coconut Shot (₹480).",
        "badge": "Party Shots"
    },
    {
        "category": "bar-mixology",
        "name": "Fine Domestic & Imported Wines",
        "type": "bar",
        "price": "₹440 – ₹730 / Glass",
        "desc": "Sula Brut (₹3,950/btl), Yellow Tail Shiraz (₹730/3600), Yellow Tail Chardonnay (₹730/3600), The Source Rosé (₹570/2800), Sula Zinfandel (₹520/2550).",
        "badge": "Curated Wine Cellar"
    }
]

# Generate HTML card for each item
cards_html = []
for item in menu_data:
    cat = item["category"]
    name = item["name"]
    itype = item["type"]
    price = item["price"]
    desc = item["desc"]
    badge = item.get("badge", "White Lotus Special")
    
    badge_type_html = ""
    if itype == "veg":
        badge_type_html = '<span class="diet-badge-veg" title="Vegetarian"></span>'
    elif itype == "nonveg":
        badge_type_html = '<span class="diet-badge-nonveg" title="Non-Vegetarian"></span>'
    elif itype == "bar":
        badge_type_html = '<span class="diet-badge-bar">🍸</span>'

    card = f'''          <!-- ITEM: {name} -->
          <div class="menu-item-row p-5 rounded-2xl bg-white shadow-sm flex flex-col justify-between" data-category="{cat}">
            <div>
              <div class="flex items-start justify-between gap-3">
                <div class="flex items-center gap-2">
                  {badge_type_html}
                  <h4 class="font-serif text-lg font-bold text-botanical-deep group-hover:text-gold transition-colors">{name}</h4>
                </div>
                <span class="font-serif text-base font-bold text-botanical-deep shrink-0">{price}</span>
              </div>
              <p class="text-xs text-charcoal/70 leading-relaxed mt-2 font-normal">
                {desc}
              </p>
            </div>
            <div class="pt-3 mt-4 border-t border-gold/15 flex items-center justify-between text-[11px]">
              <span class="text-gold font-bold uppercase tracking-wider">{badge}</span>
              <button onclick="openBookingModal()" class="text-botanical-deep hover:text-gold font-bold uppercase tracking-wider">Reserve Table &rarr;</button>
            </div>
          </div>'''
    cards_html.append(card)

menu_deck_html = "\n\n".join(cards_html)

# Navigation tabs HTML
tabs_html = '''        <!-- CATEGORY NAVIGATION TABS -->
        <div class="flex flex-wrap items-center justify-center gap-2 mb-10">
          <button onclick="filterMenu('all')" class="menu-tab-btn active px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider transition-all bg-botanical-deep text-white shadow-sm border border-gold/30" data-cat="all">
            All Curations
          </button>
          <button onclick="filterMenu('appetizers')" class="menu-tab-btn px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider transition-all bg-white text-botanical-deep hover:bg-silk shadow-sm border border-gold/20" data-cat="appetizers">
            Appetizers & Meat on Stick
          </button>
          <button onclick="filterMenu('soups-salads-bao')" class="menu-tab-btn px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider transition-all bg-white text-botanical-deep hover:bg-silk shadow-sm border border-gold/20" data-cat="soups-salads-bao">
            Soups, Salads, Munchies & Bao
          </button>
          <button onclick="filterMenu('pizza-pasta-risotto')" class="menu-tab-btn px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider transition-all bg-white text-botanical-deep hover:bg-silk shadow-sm border border-gold/20" data-cat="pizza-pasta-risotto">
            Pizzas, Pasta & Risotto
          </button>
          <button onclick="filterMenu('bowls-continental')" class="menu-tab-btn px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider transition-all bg-white text-botanical-deep hover:bg-silk shadow-sm border border-gold/20" data-cat="bowls-continental">
            Khao Suey, Bowls & Steaks
          </button>
          <button onclick="filterMenu('mains')" class="menu-tab-btn px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider transition-all bg-white text-botanical-deep hover:bg-silk shadow-sm border border-gold/20" data-cat="mains">
            Main Course (Veg & Non-Veg)
          </button>
          <button onclick="filterMenu('breads-rice-noodles')" class="menu-tab-btn px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider transition-all bg-white text-botanical-deep hover:bg-silk shadow-sm border border-gold/20" data-cat="breads-rice-noodles">
            Breads, Biryanis & Wok
          </button>
          <button onclick="filterMenu('desserts-icecream')" class="menu-tab-btn px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider transition-all bg-white text-botanical-deep hover:bg-silk shadow-sm border border-gold/20" data-cat="desserts-icecream">
            Desserts & Natural Ice Cream
          </button>
          <button onclick="filterMenu('bar-mixology')" class="menu-tab-btn px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider transition-all bg-white text-botanical-deep hover:bg-silk shadow-sm border border-gold/20" data-cat="bar-mixology">
            The Bar, Malts & Cocktails
          </button>
        </div>'''

# Complete Section replacement
new_menu_section = f'''    <!-- SECTION 3: THE OFFICIAL WHITE LOTUS CULINARY & BAR DECK -->
    <section id="menu" class="py-24 bg-cream relative">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <!-- Header -->
        <div class="text-center max-w-3xl mx-auto mb-10 space-y-3">
          <span class="text-xs uppercase tracking-[0.25em] text-gold font-bold">100% Official Gastronomy</span>
          <h2 class="font-serif text-3xl sm:text-5xl font-normal text-botanical-deep">
            The White Lotus <span class="italic font-normal">Dining & Bar Deck</span>
          </h2>
          <p class="text-sm sm:text-base text-charcoal/75 leading-relaxed">
            Directly from our floor kitchen on Saras Baug Road. Zero stock imagery. Explore our complete authentic culinary repertoire across 8 specialized sections.
          </p>
        </div>

{tabs_html}

        <!-- SEARCH & DIETARY FILTER BAR -->
        <div class="max-w-xl mx-auto mb-10 flex flex-col sm:flex-row items-center gap-3">
          <div class="relative w-full">
            <input type="text" id="menu-search-input" onkeyup="searchMenuItems()" placeholder="Instant search (e.g. Indri, Khao Suey, Loncha, Tiramisu, Pomfret, Steak, Blue Label...)" class="w-full pl-10 pr-4 py-2.5 rounded-full bg-white border border-gold/30 text-xs focus:outline-none focus:border-gold shadow-sm">
            <svg class="w-4 h-4 text-gold absolute left-3.5 top-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </div>
          <div class="flex items-center gap-3 text-xs font-semibold shrink-0">
            <span class="flex items-center gap-1.5"><span class="diet-badge-veg"></span> Pure Veg</span>
            <span class="flex items-center gap-1.5"><span class="diet-badge-nonveg"></span> Non-Veg</span>
            <span class="flex items-center gap-1.5"><span class="diet-badge-bar">🍸</span> Bar</span>
          </div>
        </div>

        <!-- COMPREHENSIVE OFFICIAL TEXT-BASED MENU GRID -->
        <div id="menu-deck-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
{menu_deck_html}
        </div>

        <!-- Download Full Menu CTA -->
        <div class="mt-14 text-center">
          <div class="inline-flex flex-col sm:flex-row items-center gap-4 p-4 rounded-2xl bg-white border border-gold/25 shadow-sm">
            <span class="text-xs text-charcoal/80 font-medium">Looking for customized banquet menus, private bottle service, or seasonal chef specials?</span>
            <a href="https://wa.me/919513575757?text=Hello%20White%20Lotus,%20please%20send%20me%20your%20complete%20PDF%20dining%20and%20cocktail%20menu." target="_blank" rel="noopener" class="px-5 py-2.5 bg-botanical-deep text-white text-xs font-bold uppercase tracking-wider rounded-xl hover:bg-botanical-surface transition-all flex items-center gap-2">
              <svg class="w-4 h-4 text-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
              <span>WhatsApp Floor Captain Desk</span>
            </a>
          </div>
        </div>

      </div>
    </section>'''

# Read index.html and replace section
with open("C:/Users/Admin/.gemini/antigravity/scratch/white-lotus-pune/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Pattern to replace from <!-- SECTION 3: to <!-- SECTION 4:
pattern = r'<!-- SECTION 3:.*?<!-- SECTION 4:'
replacement = new_menu_section + "\n\n    <!-- SECTION 4:"

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("C:/Users/Admin/.gemini/antigravity/scratch/white-lotus-pune/index.html", "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Successfully injected {len(menu_data)} authentic dishes into index.html!")
