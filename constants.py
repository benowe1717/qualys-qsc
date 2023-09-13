#!/usr/bin/env python3

COUNTRIES_WITH_STATES = [
    "United States of America", "Australia", "Canada", "India"
]

VALID_COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Anguilla", "Antartica", "Antigua and Barbuda",
    "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh",
    "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bosnia-Herzegovina",
    "Botswana", "Bouvet Island", "Brazil", "British Indian Ocean Territory", "Brunei Darussalam", "Bulgaria",
    "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands",
    "Central African Republic", "Chad", "Chile", "China", "Christmas Island", "Cocos (Keeling) Islands", "Colombia",
    "Comoros", "Congo", "Cook Islands", "Costa Rica", "Cote D'Ivoire", "Croatia", "Cuba", "Cyprus", "Czech Republic",
    "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador",
    "Equatorial Guinea", "Estonia", "Ethiopia", "Faeroe Islands", "Falkland Islands (Malvinas)", "Fiji", "Finland",
    "France", "French Guiana", "French Polynesia", "French Southern Territories", "Gabon", "Gambia", "Georgia",
    "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guatemala", "Guernsey, C.I.",
    "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard and McDonald Islands", "Honduras", "Hong Kong",
    "Hungary", "Iceland", "India", "Indonesia", "Iran (Islamic Republic of)", "Iraq", "Ireland", "Isle of Man", "Israel",
    "Italy", "Jamaica", "Japan", "Jersey, C.I.", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea", "Kuwait",
    "Kyrgyzstan", "Lao Peoples Democratic Republic", "Latvia", "Lebanon", "Lesotho", "Liberia",
    "Libyan Arab Jamahiriya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia", "Madagascar",
    "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Martinique", "Mauritania", "Mauritius",
    "Mexico", "Micronesia, Fed. States of", "Moldova, Republic of", "Monaco", "Mongolia", "Montserrat", "Morocco",
    "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherland Antilles", "Netherlands",
    "Neutral Zone (Saudi/Iraq)", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue",
    "Norfolk Island", "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palau", "Panama Canal Zone",
    "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico",
    "Qatar", "Reunion", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Samoa", "San Marino",
    "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Seychelles", "Sierra Leone", "Singapore", "Slovak Republic",
    "Slovenia", "Solomon Islands", "Somalia", "South Africa", "Spain", "Sri Lanka", "St. Helena",
    "St. Pierre and Miquelon", "St. Vincent and the Grenadines", "Sudan", "Suriname",
    "Svalbard and Jan Mayen Islands", "Swaziland", "Sweden", "Switzerland", "Syrian Arab Republic", "Taiwan",
    "Tajikistan", "Tanzania, United Republic of", "Thailand", "Togo", "Tokelau", "Tonga", "Trinidad and Tobago",
    "Tunisia", "Turkey", "Turkmenistan", "Turks and Caicos Islands", "Tuvalu", "U.S.Minor Outlying Islands",
    "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States of America", "Uruguay",
    "Uzbekistan", "Vanuatu", "Vatican City State", "Venezuela", "Vietnam", "Virgin Islands (British)",
    "Wallis and Futuna Islands", "Western Sahara", "Yemen", "Yugoslavia", "Zaire", "Zambia", "Zimbabwe"
]

VALID_US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "Armed Forces Asia", "Armed Forces Europe", "Armed Forces Pacific",
    "California", "Colorado", "Connecticut", "Delaware", "District of Columbia","Florida", "Georgia", "Hawaii",
    "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
    "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island","South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

VALID_AUS_STATES = [
    "New South Wales", "Northern Territory", "Queensland", "Tasmania", "Victoria", "Western Australia",
]

VALID_CAN_STATES = [
    "Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland",
    "Northwest Territories", "Nova Scotia", "Nunavut", "Ontario", "Prince Edward Island", "Quebec",
    "Saskatchewan", "Yukon"
]

VALID_IN_STATES = [
    "Andhra Pradesh", "Andaman and Nicobar Islands", "Arunachal Pradesh", "Assam", "Bihar",
    "Chandigarh", "Chattisgarh", "Dadra and Nagar Haveli", "Daman and Diu", "Delhi", "Goa", "Gujarat", "Haryana",
    "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Lakshadadweep",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Orissa", "Pondicherry",
    "Punjab", "Rajasthan","Sikkim", "Tamil Nadu", "Tripura", "Uttar Pradesh", "Uttaranchal", "West Bengal"
]

REQUIRED_FIELDS = [
    "user_role", "business_unit", "first_name", "last_name", "title", "phone", "email", "address1", "city", "country", "state"
]

GLOBAL_TAG = "QSC"
NEEDLE = "EC2"
DECODERS = [
    "ISO-8859-1", "utf-8", "unicode_escape"
]