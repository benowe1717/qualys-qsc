#!/usr/bin/env python3

# argparse
ARGPARSE_PROGRAM_NAME = 'main.py'
ARGPARSE_PROGRAM_DESCRIPTION = 'Qualys QSC Hands-on Training is a `tool` '
ARGPARSE_PROGRAM_DESCRIPTION += 'that allows `administrators/trainers` to '
ARGPARSE_PROGRAM_DESCRIPTION += '`provision accounts in a Qualys subscription'
ARGPARSE_PROGRAM_DESCRIPTION += '.`'
ARGPARSE_PROGRAM_VERSION = '0.0.6'
ARGPARSE_PROGRAM_AUTHOR = 'Benjamin Owen'
ARGPARSE_PROGRAM_REPO = 'https://github.com/benowe1717/qualys-qsc'

# qualys_api
QUALYS_API_CREDENTIALS_KEYS = ['username', 'password', 'host']
QUALYS_API_USER_AGENT = 'Python3Requests'
QUALYS_API_CONTENT_TYPE = 'application/x-www-form-urlencoded'
QUALYS_API_SCHEME = 'https://'
QUALYS_API_REQUIRED_USER_FIELDS = {
    'action': 'add',
    'user_role': 'reader',
    'business_unit': 'Unassigned',
    'first_name': 'QSC',
    'last_name': 'Training',
    'title': 'QSC Training 2023',
    'phone': '18007454355',
    'email': 'qsc-training@qualys.com',
    'address1': '919 E Hillsdale Blvd, 4th floor',
    'city': 'Foster City',
    'country': 'United States of America',
    'state': 'California',
    'send_email': 0
}
QUALYS_API_OPTIONAL_USER_FIELDS = [
    'asset_groups', 'fax', 'address2', 'zip_code', 'external_id'
]
QUALYS_API_VALID_USER_ROLES = [
    'manager', 'unit_manager', 'scanner', 'reader', 'contact', 'administrator'
]
QUALYS_API_VALID_COUNTRY_CODES = [
    'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Anguilla',
    'Antartica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba',
    'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh',
    'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan',
    'Bolivia', 'Bosnia-Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil',
    'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria',
    'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
    'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China',
    'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros',
    'Congo', 'Cook Islands', 'Costa Rica', "Cote D'Ivoire", 'Croatia', 'Cuba',
    'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica',
    'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador',
    'Equatorial Guinea', 'Estonia', 'Ethiopia', 'Faeroe Islands',
    'Falkland Islands (Malvinas)', 'Fiji', 'Finland', 'France',
    'French Guiana', 'French Polynesia', 'French Southern Territories',
    'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece',
    'Greenland', 'Grenada', 'Guadeloupe', 'Guatemala', 'Guernsey, C.I.',
    'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti',
    'Heard and McDonald Islands', 'Honduras', 'Hong Kong', 'Hungary',
    'Iceland', 'India', 'Indonesia', 'Iran (Islamic Republic of)', 'Iraq',
    'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan',
    'Jersey, C.I.', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea',
    'Kuwait', 'Kyrgyzstan', 'Lao Peoples Democratic Republi', 'Latvia',
    'Lebanon', 'Lesotho', 'Liberia', 'Libyan Arab Jamahiriya', 'Liechtenstein',
    'Lithuania', 'Luxembourg', 'Macau', 'Macedonia', 'Madagascar', 'Malawi',
    'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
    'Mauritania', 'Mauritius', 'Mexico', 'Micronesia, Fed. States of',
    'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montserrat', 'Morocco',
    'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal',
    'Netherland Antilles', 'Netherlands', 'Neutral Zone (Saudi/Iraq)',
    'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue',
    'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan',
    'Palau', 'Panama', 'Panama Canal Zone', 'Papua New Guinea', 'Paraguay',
    'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico',
    'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis',
    'Saint Lucia', 'Samoa', 'San Marino', 'Sao Tome and Principe',
    'Saudi Arabia', 'Senegal', 'Seychelles', 'Sierra Leone', 'Singapore',
    'Slovak Republic', 'Slovenia', 'Solomon Islands', 'Somalia',
    'South Africa', 'Spain', 'Sri Lanka', 'St. Helena',
    'St. Pierre and Miquelon', 'St. Vincent and the Grenadines', 'Sudan',
    'Suriname', 'Svalbard and Jan Mayen Islands', 'Swaziland', 'Sweden',
    'Switzerland', 'Syrian Arab Republic', 'Taiwan', 'Tajikistan',
    'Tanzania, United Republic of', 'Thailand', 'Togo', 'Tokelau', 'Tonga',
    'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan',
    'Turks and Caicos Islands', 'Tuvalu', 'U.S.Minor Outlying Islands',
    'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom',
    'United States of America', 'Uruguay', 'Uzbekistan', 'Vanuatu',
    'Vatican City State', 'Venezuela', 'Vietnam', 'Virgin Islands (British)',
    'Wallis and Futuna Islands', 'Western Sahara', 'Yemen', 'Yugoslavia',
    'Zaire', 'Zambia', 'Zimbabwe'
]
QUALYS_API_VALID_US_STATES = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Armed Forces',
    'Armed Forces Asia', 'Armed Forces Europe', 'California', 'Colorado',
    'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia',
    'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
    'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
    'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
    'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
    'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pacific', 'Pennsylvania',
    'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
    'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin',
    'Wyoming'
]
QUALYS_API_VALID_AUS_STATES = [
    'No State', 'New South Wales', 'Northern Territory', 'Queensland',
    'Tasmania', 'Victoria', 'Western Australia'
]
QUALYS_API_VALID_CAN_STATES = [
    'No State', 'Alberta', 'British Columbia', 'Manitoba', 'New Brunswick',
    'Newfoundland', 'Northwest Territories', 'Nova Scotia', 'Nunavut',
    'Ontario', 'Price Edward Island', 'Quebec', 'Saskatchewan', 'Yukon'
]
QUALYS_API_VALID_IN_STATES = [
    'Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh',
    'Assam', 'Bihar', 'Chandigarh', 'Chattisgarh', 'Dadra and Nagar Haveli',
    'Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh',
    'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Lakshadadweep',
    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
    'Nagaland', 'No State', 'Orissa', 'Pondicherry', 'Punjab', 'Rajasthan',
    'Sikkim', 'Tamil Nadu', 'Tripura', 'Uttar Pradesh', 'Uttaranchal',
    'West Benga'
]
QUALYS_API_USERNAME_FORMAT = 'quays'

# mailmerge
MAILMERGE_TEMPLATE_KEYS = [
    'email', 'username', 'password', 'url'
]
MAILMERGE_SERVER_KEYS = [
    'host', 'port', 'username', 'security', 'ratelimit'
]
