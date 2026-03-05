from typing import Literal

UserMenuOption = Literal[
    "Your Profile",
    "Settings",
    "Log Out",
]

MainNavOption = Literal[
    "Funnels",
    "Templates",
    "Analytics",
    "Integrations",
    "A/B Tests",
    "Automations",
    "Leads",
]

FunnelMenuOption = Literal[
    "View",
    "Preview",
    "Edit",
    "Configure",
    "Connect",
    "Share & embed",
    "Responses",
    "Publish now",
    "Move to workspace",
    "Duplicate funnel",
    "Delete funnel",
]

SortTypes = Literal[
    "submissions-asc",
    "submissions-desc",
    "name-asc",
    "name-desc",
    "created-asc",
    "created-desc",

]

SortOrder = Literal[
    "asc",
    "desc"
]

FunnelTypes = Literal[
    "Thank You page",
    "Answer-based Outcomes",
    "Score-based Outcomes"
]

Elements = Literal[
    'Single Choice', 'Multiple Choice', 'Yes/No', 'Single Image Choice', 'Multiple Image Choice',
    'Dropdown', 'Rating', 'Slider', 'Net Promoter Score ®', 'Short Answer', 'Long Answer',
    'Number Input', 'Currency', 'Autocomplete', 'File Upload', 'Personalized AI Text',
    'Variable', 'Contact Form', 'Email', 'Phone', 'Address', 'Country', 'Website', 'Opt-In Checkbox',
    'Captcha', 'E-Signature', 'Date & Time', 'Schedule Appointments', 'Page Timer', 'Button', 'Back Link',
    'Skip Link', 'Divider', 'Spacer', 'Loader', 'Print page', 'Save as PDF', 'Heading', 'Paragraph',
    'Image + Text', 'Image', 'Video', 'Widget Embed', 'Google Maps', 'Airtable', 'Social Share',
    'Social Links', 'Coupon Code', 'Price Calculator', 'Collect Payments', 'Calculator', 'Score',
    'Outcome Distribution', 'Answer Summary']

FunnelStatus = Literal[
    "Published",
    "Completed",
    "Archived",
    "Draft",
    "All"
]

TextChoiceOptions = Literal[
    "Hide question text for participants",
    "Answer is required",
    "Randomize answers",
    "Individual Score & Calculation",
    "Always Hide for participants",
]

TextAnswerOptions = Literal[
    "Continue by pressing enter",
    "Hide question text for participants",
    "Use question as placeholder",
    "Answer is required",
    "Only accept numbers",
    "Always Hide for participants"

]

SliderOptions = Literal[
    "Min Value",
    "Max Value",
    "Start Value",
]


PageMenuOption = Literal[
    "Move right",
    "Move left",
    "Edit",
    "Duplicate",
    "Disable",
    "Delete",
]

QuestionTypes = Literal[
    "Text Choice",
    "Image Choice",
    "Dropdown"
]

ElementTextBox = Literal[
    "Question Text",
    "Description Text",
    "Hint / Help Text",
]

EditorHeaderOpt = Literal[
    "Edit",
    "Connect",
    "Settings",
    "Share & Embed",
    "Responses",
]
