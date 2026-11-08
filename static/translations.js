// static/translations.js

const globalTranslations = {
    'en': {
        // Sidebar & Navigation
        'dashboard': 'Dashboard',
        'request_doc': 'Request Document',
        'apply_permit': 'Apply for Permit',
        'my_requests': 'My Requests',
        'events': 'Events Calendar',
        'announcements': 'Announcements',
        'settings': 'Settings',
        'logout': 'Logout',
        'about_us': 'About Us',
        'faqs': 'FAQs',
        
        // Dashboard Quick Actions
        'track_requests': 'Track Requests',
        'track_requests_desc': 'Check status of applications',
        'barangay_map': 'Barangay Map',
        'barangay_map_desc': 'Locate health centers, evacuation sites',
        'welcome_back': 'Welcome back',

        // About Us Page
        'about_subtitle': 'Get to know your Barangay Sto. Niño Online Services Portal',
        'welcome_title': 'Welcome to Barangay Sto. Niño Online Services Portal',
        'welcome_p1': 'Our goal is to make the process of obtaining documents and submitting permit applications easier, faster, and more reliable for all residents of Barangay Sto. Niño.',
        'welcome_p2': 'Through this online portal, you no longer have to wait in long lines at the barangay hall. You can request documents and apply for permits right from the comfort of your home.',
        'our_mission': 'Our Mission',
        'mission_text': 'To provide efficient, transparent, and accessible government services to every resident of Barangay Sto. Niño through digital innovation and good governance.',
        'our_vision': 'Our Vision',
        'vision_text': 'A progressive, united, and digitally-empowered barangay where every citizen has easy access to quality public service.',
        'services_offered': 'Services Offered',
        'service_clearance': 'Barangay Clearance',
        'service_clearance_desc': 'For employment, business, and other transactions.',
        'service_indigency': 'Certificate of Indigency',
        'service_indigency_desc': 'For medical and financial assistance.',
        'service_residency': 'Certificate of Residency',
        'service_residency_desc': 'Proof of residence in the barangay.',
        'service_event': 'Community Event Permits',
        'service_event_desc': 'For private occasions and activities.',
        'contact_info': 'Contact Information',
        'address': 'Address',
        'email': 'Email',
        'phone': 'Phone',
        'office_hours': 'Office Hours',
        'office_hours_value': 'Mon - Fri: 8:00 AM - 5:00 PM',
        
        // FAQs Page
        'faq_title': 'Frequently Asked Questions',
        'faq_subtitle': 'Find answers to common questions about our services',
        'faq_q1': 'How do I change my password?',
        'faq_a1': 'If you are on the Login page: Click "Forgot Password?" below the login fields. Enter your registered email address and your desired new password. Make sure all information is correct before confirming. If you are already logged in: Click your Profile in the upper-right corner. Select the option to Change Password. Enter your registered email address and desired new password.',
        'faq_q2': 'Can I change my email address?',
        'faq_a2': 'No. Your email address is permanent once your account has been created and cannot be changed.',
        'faq_q3': 'Can I delete my account?',
        'faq_a3': 'No. Account deletion is currently not available.',
        'faq_q4': 'What should I do if my account has been hacked?',
        'faq_a4': 'If you believe that your account has been hacked, contact the Barangay Sto. Niño Help Desk for assistance. Contact Number: 0992 225 0927. Office Hours: 8:00 AM – 5:00 PM, Monday to Friday.',
        'faq_q5': 'What is this website for?',
        'faq_a5': 'The Barangay Sto. Niño Online Services website makes common barangay services easier to access online. Residents can use the website to: Request Barangay Clearance, Certificate of Indigency, Proof of Residency, Apply for Community Event Permits, Track the status of their requests.',
        'faq_q6': 'How do I apply for a Barangay Clearance, Certificate of Indigency, or Proof of Residency?',
        'faq_a6': 'From your Dashboard, go to Quick Actions. Click "Request Document." Select the document you want to request. Fill out all required information. Read and agree to the Terms and Conditions. Click "Submit Request." Take note of your Reference Number.',
        'faq_q7': 'Can a minor apply for a Barangay Clearance, Certificate of Indigency, or Proof of Residency?',
        'faq_a7': 'Yes, but a parent or legal guardian must accompany the minor and sign the document request form on their behalf.',
        'faq_q8': 'What is an Area Representative?',
        'faq_a8': 'An Area Representative is a designated official who verifies the residency and identity of applicants within a specific zone or area in the barangay.',
        'faq_q9': 'How do I get the signature of the Area Representative?',
        'faq_a9': 'You can visit the Barangay Hall to locate your area representative, or upload a scanned copy of their signature if you already have it. The request will not be processed without this signature.',
        'faq_q10': 'Who can be my reference person?',
        'faq_a10': 'Any adult resident of Barangay Sto. Niño who can vouch for your identity and residency, such as a neighbor, employer, or barangay official.',
        'faq_q11': 'How long must I have lived in Barangay Sto. Niño to request a Proof of Residency?',
        'faq_a11': 'You must be a bonafide resident of the barangay. There is no strict minimum number of years, but you must be able to prove your current address.',
        'faq_q12': 'What if I do not have a Precinct Number?',
        'faq_a12': 'You can leave it blank or write "N/A" if you are not yet a registered voter in the barangay.',
        'faq_q13': 'Where is the Barangay Sto. Niño Office, and how can I contact them?',
        'faq_a13': 'The office is located at the Barangay Hall. You can contact them via phone at 0992 225 0927 or email them at barangay.stonino@email.com.',
        'faq_q14': 'How do I claim my Barangay Clearance, Certificate of Indigency, or Proof of Residency?',
        'faq_a14': 'Once your request is approved, you will receive a notification. Bring a valid ID and your Reference Number to the Barangay Hall to claim your document.',
        'faq_q15': 'Where can I find my Reference Number?',
        'faq_a15': 'Your Reference Number is displayed immediately after you submit a request, and it is also visible in the "My Requests" page.',
        'faq_q16': 'How do I apply for an Event Permit?',
        'faq_a16': 'Go to "Apply for Permit" on the sidebar. Fill out the event details, upload the required documents, and submit it at least 10 days before the event.',
        'faq_q17': 'How can I track the status of my request or application?',
        'faq_a17': 'Go to the "My Requests" page on the sidebar to see if your request is Pending, Approved, or Rejected.',
        'faq_q18': 'Where can I check venue availability?',
        'faq_a18': 'You can check the "Events Calendar" on the sidebar to see if the date and venue you want are already booked by another event.',
        'faq_q19': 'Where are the available venues and courts located?',
        'faq_a19': 'Common venues include the Barangay Covered Court, Multi-Purpose Hall, and nearby basketball courts. Please visit the Barangay Hall for specific reservations.',
        
        // Request Document Page
        'doc_title': 'Document Request Form',
        'doc_subtitle': 'Submit a request for barangay documents',
        'doc_type': 'Document Type',
        'select_doc': 'Select Document Type',
        'personal_info': 'Personal Information',
        'surname': 'Surname',
        'given_name': 'Given Name',
        'middle_name': 'Middle Name',
        'address_label': 'Address',
        'phone_label': 'Phone Number',
        'civil_status': 'Civil Status',
        'age': 'Age',
        'dob': 'Date of Birth',
        'precinct': 'Precinct No.',
        'pob': 'Place of Birth',
        'length_stay': 'Length of Stay in Barangay',
        'residency': 'Residency Type',
        'owner': 'Owner',
        'renter': 'Renter',
        'sharer': 'Sharer',
        'property_deed': 'Name on the Property Deed',
        'owner_address': "Owner's Address",
        'family_info': 'Family Information',
        'father': 'Name of Father',
        'mother': 'Name of Mother',
        'spouse': 'Name of Spouse',
        'occupation': 'Occupation',
        'emergency': 'In Case of Emergency',
        'emergency_no': 'Emergency Contact No.',
        'ref_person': 'Reference Person',
        'ref1_name': 'Reference 1 - Name',
        'ref1_address': 'Reference 1 - Address',
        'ref2_name': 'Reference 2 - Name',
        'ref2_address': 'Reference 2 - Address',
        'purpose_sig': 'Purpose & Signature',
        'purpose_doc': 'Purpose of Securing Document',
        'printed_name': 'Printed Name (Digital Signature)',
        'date': 'Date',
        'terms': 'Terms and Conditions',
        'submit_req': 'Submit Request',
        'clear_form': 'Clear Form',
        'area_rep_section': 'Area Representative Signature',
        'select_rep_position': 'Select Area Representative Position',
        'upload_signature': 'Upload a Signature of Area Representative',
        'signature_note': 'Please upload a clear signature of the Area Representative above their printed name with the date signed below.',
        'digital_signature_consent': 'By typing my printed name above, I acknowledge that this serves as my digital signature, and I agree to the terms and conditions stated in this document request.',
        'data_privacy_consent': 'I hereby give my informed consent for the Barangay Sto. Niño to collect, store, and process my personal information in accordance with the Data Privacy Act of 2012 (RA 10173) for the sole purpose of processing my document request.',
        'important_complete_fields': 'Important: Please Complete All Required Fields',
        'complete_fields_desc': 'Make sure to fill in all information marked with * and upload the required signature before submitting.',
        
        // Apply Permit Page
        'permit_title': 'Event Permit Application',
        'permit_subtitle': 'Submit a community event permit application',
        'event_info': 'Event Information',
        'event_name': 'Event Name',
        'event_desc': 'Event Description',
        'date_time': 'Date & Time',
        'event_date': 'Event Date',
        'start_time': 'Start Time',
        'end_time': 'End Time',
        'venue_attendees': 'Venue & Attendees',
        'venue': 'Venue',
        'attendees': 'Estimated Attendees',
        'purpose': 'Purpose',
        'purpose_event': 'Purpose of Event',
        'contact_person': 'Contact Person',
        'contact_phone': 'Contact Phone',
        'supporting_doc': 'Supporting Document',
        'submit_app': 'Submit Application',
        'apply_10_days': 'Important: Apply 10 Days Before Event',
        'apply_10_days_desc': 'Please submit your application at least 10 days before the event date to allow proper processing and review by the Barangay staff.',
        'allowed_hours': 'Allowed: 8:00 AM – 10:00 PM only',
        'max_attendees': 'Maximum of 300 attendees',
        'accepted_formats': 'Accepted formats: JPG, PNG, PDF, DOC, DOCX (Max 5MB)',
        'agree_terms': 'I have read and agree to the Terms and Conditions',
        
        // My Requests Page
        'myreq_title': 'My Requests',
        'myreq_subtitle': 'Track the status of your requests and permits',
        'doc_requests': 'Document Requests',
        'event_permits': 'Event Permits',
        'doc_requests_list': 'Document Requests List',
        'event_permits_list': 'Event Permits List',
        'total_docs': 'Total Documents',
        'total_permits': 'Total Permits',
        'pending': 'Pending',
        'approved': 'Approved',
        'rejected': 'Rejected',
        'view': 'View',
        'no_doc_requests': 'No Document Requests',
        'no_doc_requests_desc': "You haven't submitted any document request yet.",
        'no_event_permits': 'No Event Permits',
        'no_event_permits_desc': "You haven't submitted any event permit application yet.",
        'document_details': 'Document Details',
        'event_permit_details': 'Event Permit Details',
        'reference_no': 'Reference No',
        'date_requested': 'Date Requested',
        'notes': 'Notes',
        'status': 'Status',
        'event_time': 'Event Time',
        'description': 'Description',
        
        // Events Page
        'events_title': 'Events Calendar',
        'events_subtitle': 'Click on a date to see event details',
        'event_details': 'Event Details',
        'loading_events': 'Loading events...',
        'no_events': 'No Events',
        'events_on_this_date': 'Events on this Date',
        'no_date_selected': 'No Date Selected',
        'click_date_details': 'Click on a date with an event to see the details here.',
        'no_approved_events': 'No approved events on this date.',
        'time_not_specified': 'Time not specified',
        'time_label': 'Time:',
        'venue_label': 'Venue:',
        'expected_attendees_label': 'Expected Attendees:',
        
        // Settings Page
        'settings_title': 'Settings',
        'settings_subtitle': 'Manage your account and system settings',
        'update_profile': 'Update Profile',
        'update_profile_desc': 'Update your personal information including name, email, and contact details.',
        'change_pass': 'Change Password',
        'change_pass_desc': 'Change your account password for better security. Use a strong password.',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'email_address': 'Email Address',
        'contact_number': 'Contact Number',
        'address_label_settings': 'Address',
        'cancel': 'Cancel',
        'save_changes': 'Save Changes',
        'current_password': 'Current Password',
        'new_password': 'New Password',
        'confirm_new_password': 'Confirm New Password',
        'update_password': 'Update Password',
        
        // Announcements Page
        'announcements_title': 'Announcements',
        'announcements_subtitle': 'Latest Barangay Sto. Niño Updates',
        'recent_announcements': 'Recent Announcements',
        'mark_all_as_read': 'Mark all as read',
        'mark_all_as_unread': 'Mark all as unread',
        'view_all_announcements': 'View All Announcements',
        'pinned': 'Pinned',
        'no_announcements': 'No Announcements Yet',
        'no_announcements_desc': "Wala pang announcement na na-post.",

                // Dagdag para sa Notification Panel
        'recent_announcements': 'Recent Announcements',
        'mark_all': 'Mark all',
        'no_recent_announcements': 'No recent announcements',
        'loading': 'Loading...',
        'all_read': 'All Read',

        // Role
        'resident': 'Resident',

        // Form Placeholders & Modal Texts
        'select_doc_placeholder': '-- Select Document Type --',
        'surname_placeholder': 'Surname',
        'given_name_placeholder': 'Given Name',
        'middle_name_placeholder': 'Middle Name',
        'complete_address_placeholder': 'Complete Address',
        'phone_placeholder': '09XXXXXXXXX',
        'age_placeholder': 'Age',
        'precinct_placeholder': 'Precinct No.',
        'pob_placeholder': 'Place of Birth',
        'length_stay_placeholder': 'e.g. 5 years',
        'occupation_placeholder': 'Occupation',
        'property_deed_placeholder': 'Name on Property Deed',
        'owner_address_placeholder': 'Address of Owner',
        'select_date_placeholder': 'Select a date...',
        'select_venue_placeholder': 'Select a venue...',
        'attendees_placeholder': 'e.g., 100',
        'event_name_placeholder': 'e.g., Barangay Basketball League',
        'event_desc_placeholder': 'Describe your event briefly...',
        'event_purpose_placeholder': 'Describe the purpose of your event...',
        'time_allowed_note': 'Allowed: 8:00 AM – 10:00 PM only',
        'max_attendees_note': 'Maximum of 300 attendees',
        'select': 'Select',
        'cancel_request_title': 'Cancel Request?',
        'cancel_request_desc': 'Are you sure you want to cancel this request?',
        'cancel_request_warning': 'This action cannot be undone.',
        'no_keep_it': 'No, Keep it',
        'yes_cancel': 'Yes, Cancel',
        
        // Bagong dagdag base sa screenshot
        'ref_name_placeholder': 'Reference Name',
        'ref_address_placeholder': 'Reference Address',
        'purpose_req_placeholder': 'State the purpose of your request...',
        'type_full_name_placeholder': 'Type your full name here',
        'signature_consent_text': 'By typing my printed name above, I acknowledge that this serves as my digital signature, and I agree to the terms and conditions stated in this document request.',
        'privacy_consent_text': 'I hereby give my informed consent for the Barangay Sto. Niño to collect, store, and process my personal information in accordance with the Data Privacy Act of 2012 (RA 10173) for the sole purpose of processing my document request.',
        'not_related_to_you': '(Not Related to You)',
        'by_typing_consent_part1': 'By typing my printed name above, I acknowledge that this serves as my',
        'by_typing_consent_part2': 'digital signature',
        'by_typing_consent_part3': ', and I agree to the terms and conditions stated in this document request.',
        'privacy_consent_part1': 'I hereby give my',
        'privacy_consent_part2': 'informed consent',
        'privacy_consent_part3': 'for the Barangay Sto. Niño to collect, store, and process my personal information in accordance with the',
        'privacy_consent_part4': 'Data Privacy Act of 2012 (RA 10173)',
        'privacy_consent_part5': 'for the sole purpose of processing my document request.',
        'father_name_placeholder': "Father's Name",
        'mother_name_placeholder': "Mother's Name",
        'spouse_name_placeholder': "Spouse's Name",
        'emergency_name_placeholder': 'Emergency Contact Name',

        // Terms and Conditions - Apply Permit
        'tc_acceptance': '1. Acceptance of Terms',
        'tc_acceptance_desc': 'By submitting this application, you agree to comply with all barangay rules and regulations regarding events and gatherings.',
        'tc_guidelines': '2. Event Guidelines',
        'tc_guidelines_desc': 'All events must adhere to the following:',
        'tc_max_attendees': 'Maximum of 300 attendees per event',
        'tc_start_time': 'Start Time: 8:00 AM - 10:00 PM',
        'tc_end_time': 'End Time: 8:00 AM - 10:00 PM',
        'tc_waste': 'Proper waste management must be observed',
        'tc_noise': 'No excessive noise beyond barangay limits',
        'tc_10_days': 'Event must be 10 days before the Event Date',
        'tc_responsibility': '3. Responsibility',
        'tc_responsibility_desc': 'The applicant is fully responsible for the event and must ensure the safety and orderliness of the activity.',
        'tc_data_privacy': '4. Data Privacy',
        'tc_data_privacy_desc': 'Your information will be used solely for permit processing and barangay records in accordance with the Data Privacy Act.',
        'tc_cancellation': '5. Cancellation Policy',
        'tc_cancellation_desc': 'Permit must be cancelled at least 3 days before the event. Failure to do so may result in penalties.',
        'tc_checkbox_text': 'I have read and agree to the Terms and Conditions of Barangay Sto. Niño',
        'choose_file': 'Choose File',
        'no_file_chosen': 'No file chosen',
        'upload_file_text': 'Choose File',

        // Calendar Days & Menu
        'sun': 'SUN',
        'mon': 'MON',
        'tue': 'TUE',
        'wed': 'WED',
        'thu': 'THU',
        'fri': 'FRI',
        'sat': 'SAT',
        'english_menu': 'us English',
        'tagalog_menu': 'ph Tagalog',
        'select_date': 'Select Date',
        'cancel_btn': 'CANCEL',

        // Dagdag na Status
        'processing': 'PROCESSING',
        'ready_for_pickup': 'READY FOR PICKUP',
        'cancelled': 'Cancelled',

        // Settings Modal Extras
        'req_length': 'At least 8 characters',
        'req_upper': 'At least 1 uppercase letter',
        'req_lower': 'At least 1 lowercase letter',
        'req_number': 'At least 1 number',
        'req_special': 'At least 1 special character (!@#$%^&*)',
        'reenter_password': 'Re-enter new password',
        'verify_update': 'Verify Profile Update',
        'enter_code_sent': 'Enter the code sent to your email',
        'six_digit_code': '6-Digit Code',
        'verify_save': 'Verify & Save',
        'invalid_code': 'Invalid code. Please try again.',
        'check_email_spam': 'Check your email inbox (and spam folder).',
        'a_6_digit_code_sent': 'A 6-digit reset code has been sent to your email. Check your inbox (and spam folder).',
        'password_changed': 'Password Changed!',
        'password_changed_desc': 'Your password has been successfully updated. A confirmation email has been sent.',
        'okay_got_it': 'Okay, Got it',
        'success_title': 'Success!',
        'profile_updated_desc': 'Profile updated successfully! A confirmation email has been sent to your inbox.',
        'sending_code': 'Sending Code...',
        'verifying': 'Verifying...',
        'verify_code': 'Verify Code',

        // Success Modals (Request & Permit)
        'request_submitted': 'Request Submitted!',
        'request_received': 'Your document request has been received',
        'permit_submitted': 'Permit Submitted!',
        'permit_received': 'Your application has been received',
        'please_wait': 'Please Wait',
        'request_pending_desc': 'Your request is now',
        'request_pending_desc_2': 'Please allow 1-2 business days for processing.',
        'permit_pending_desc': 'Your permit is now',
        'permit_pending_desc_2': 'Please allow 24 hours for the Barangay staff to review and approve your application.',
        'show_qr_code': 'Show this QR code to Barangay personnel for faster transaction.',
        'notification_ready': 'You will receive a notification once your document is ready.',
        'notification_ready_permit': 'You will receive a notification once your permit status is updated.',
        'track_status': 'Track Status',
        'submit_another': 'Submit Another',
        'request_another': 'Request Another',
        'document_label': 'DOCUMENT:',
        'applicant_label': 'APPLICANT:',
        'event_label': 'EVENT:',
        'date_label': 'DATE:',
        'time_label_modal': 'ORAS:',
        'venue_label_modal': 'LUGAR:',
        'status_label': 'STATUS:',
        'please_save_number': 'Please save this number for tracking'
    },
    'tl': {
        // Sidebar & Navigation
        'dashboard': 'Dashboard',
        'request_doc': 'Mag-request ng Dokumento',
        'apply_permit': 'Mag-apply ng Permit',
        'my_requests': 'Aking mga Request',
        'events': 'Kalendaryo ng mga Kaganapan',
        'announcements': 'Mga Anunsyo',
        'settings': 'Settings',
        'logout': 'Mag-logout',
        'about_us': 'Tungkol Sa Amin',
        'faqs': 'Mga FAQ',
        
        // Dashboard Quick Actions
        'track_requests': 'I-track ang mga Request',
        'track_requests_desc': 'Tingnan ang status ng mga aplikasyon',
        'barangay_map': 'Mapa ng Barangay',
        'barangay_map_desc': 'Hanapin ang mga health center at evacuation site',
        'welcome_back': 'Maligayang Pagbabalik',

        // About Us Page
        'about_subtitle': 'Kilalanin ang Barangay Sto. Niño Online Services Portal',
        'welcome_title': 'Maligayang Pagdating sa Barangay Sto. Niño Online Services Portal',
        'welcome_p1': 'Layunin namin na gawing mas madali, mas mabilis, at mas maaasahan ang proseso ng pagkuha ng mga dokumento at pagsusumite ng permit para sa lahat ng residente ng Barangay Sto. Niño.',
        'welcome_p2': 'Sa pamamagitan ng online portal na ito, hindi mo na kailangang pumila nang matagal sa barangay hall. Maaari kang mag-request ng dokumento at mag-apply ng permit mula sa iyong tahanan.',
        'our_mission': 'Aming Misyon',
        'mission_text': 'Magbigay ng mahusay, transparent, at accessible na serbisyo ng gobyerno sa bawat residente ng Barangay Sto. Niño sa pamamagitan ng digital innovation at good governance.',
        'our_vision': 'Aming Bisyon',
        'vision_text': 'Isang progresibo, nagkakaisa, at digital na barangay kung saan ang bawat mamamayan ay may madaling access sa dekalidad na pampublikong serbisyo.',
        'services_offered': 'Mga Serbisyong Inaalok',
        'service_clearance': 'Barangay Clearance',
        'service_clearance_desc': 'Para sa trabaho, negosyo, at iba pang transaksyon.',
        'service_indigency': 'Certificate of Indigency',
        'service_indigency_desc': 'Para sa medikal at pinansyal na tulong.',
        'service_residency': 'Certificate of Residency',
        'service_residency_desc': 'Patunay ng paninirahan sa barangay.',
        'service_event': 'Mga Permit sa Kaganapan',
        'service_event_desc': 'Para sa mga pribadong okasyon at aktibidad.',
        'contact_info': 'Impormasyon ng Contact',
        'address': 'Tirahan',
        'email': 'Email',
        'phone': 'Telepono',
        'office_hours': 'Oras ng Opisina',
        'office_hours_value': 'Lunes - Biyernes: 8:00 AM - 5:00 PM',
        
        // FAQs Page
        'faq_title': 'Mga Madalas Itanong',
        'faq_subtitle': 'Maghanap ng sagot sa mga karaniwang tanong tungkol sa aming serbisyo',
        'faq_q1': 'Paano ko babaguhin ang aking password?',
        'faq_a1': 'Kung nasa Login page ka: I-click ang "Forgot Password?" sa ibaba ng login fields. Ilagay ang iyong registered email address at ang nais na bagong password. Siguraduhing tama ang lahat ng impormasyon bago kumpirmahin. Kung naka-login ka na: I-click ang iyong Profile sa kanang sulok sa itaas. Piliin ang opsyong Change Password. Ilagay ang iyong registered email address at nais na bagong password.',
        'faq_q2': 'Maaari ko bang baguhin ang aking email address?',
        'faq_a2': 'Hindi. Ang iyong email address ay permanente na kapag na-create na ang iyong account at hindi na maaaring baguhin.',
        'faq_q3': 'Maaari ko bang i-delete ang aking account?',
        'faq_a3': 'Hindi. Ang pag-delete ng account ay kasalukuyang hindi available.',
        'faq_q4': 'Ano ang dapat kong gawin kung na-hack ang aking account?',
        'faq_a4': 'Kung sa tingin mo ay na-hack ang iyong account, makipag-ugnayan sa Barangay Sto. Niño Help Desk para sa tulong. Numero ng Contact: 0992 225 0927. Oras ng Opisina: 8:00 AM – 5:00 PM, Lunes hanggang Biyernes.',
        'faq_q5': 'Para saan ang website na ito?',
        'faq_a5': 'Ginagawang mas madaling ma-access online ng Barangay Sto. Niño Online Services website ang mga karaniwang serbisyo ng barangay. Maaaring gamitin ng mga residente ang website upang: Mag-request ng Barangay Clearance, Certificate of Indigency, Proof of Residency, Mag-apply ng Community Event Permits, Tingnan ang status ng kanilang mga request.',
        'faq_q6': 'Paano ako mag-a-apply para sa Barangay Clearance, Certificate of Indigency, o Proof of Residency?',
        'faq_a6': 'Mula sa iyong Dashboard, pumunta sa Quick Actions. I-click ang "Request Document." Piliin ang dokumentong nais mong i-request. Punan ang lahat ng kinakailangang impormasyon. Basahin at sumang-ayon sa Terms and Conditions. I-click ang "Submit Request." Tandaan ang iyong Reference Number.',
        'faq_q7': 'Maaari bang mag-apply ang isang menor de edad para sa Barangay Clearance, Certificate of Indigency, o Proof of Residency?',
        'faq_a7': 'Oo, ngunit kailangang samahan ng magulang o legal na tagapag-alaga ang menor de edad at sila ang pipirma sa form.',
        'faq_q8': 'Ano ang Area Representative?',
        'faq_a8': 'Ang Area Representative ay isang itinalagang opisyal na nagbe-verify ng paninirahan at pagkakakilanlan ng mga aplikante sa isang partikular na lugar sa barangay.',
        'faq_q9': 'Paano ko makukuha ang lagda ng Area Representative?',
        'faq_a9': 'Maaari kang pumunta sa Barangay Hall para hanapin ang iyong area representative, o mag-upload ng scanned na kopya ng kanilang lagda kung mayroon ka na. Hindi ipoproseso ang request kung walang lagda.',
        'faq_q10': 'Sino ang pwedeng maging reference person ko?',
        'faq_a10': 'Kahit sinong nasa hustong gulang na residente ng Barangay Sto. Niño na makakapagpatunay ng iyong pagkakakilanlan at paninirahan, tulad ng kapitbahay, amo, o barangay official.',
        'faq_q11': 'Gaano katagal akong dapat nakatira sa Barangay Sto. Niño para makakuha ng Proof of Residency?',
        'faq_a11': 'Kailangan mong maging ganap na residente ng barangay. Walang mahigpit na minimum na taon, ngunit kailangan mong mapatunayan ang iyong kasalukuyang tirahan.',
        'faq_q12': 'Paano kung wala akong Precinct Number?',
        'faq_a12': 'Maaari mong iwanan itong blangko o isulat ang "N/A" kung hindi ka pa rehistradong botante sa barangay.',
        'faq_q13': 'Saan matatagpuan ang Barangay Sto. Niño Office, at paano ako makikipag-ugnayan?',
        'faq_a13': 'Ang opisina ay matatagpuan sa Barangay Hall. Maaari kang makipag-ugnayan sa pamamagitan ng telepono sa 0992 225 0927 o mag-email sa barangay.stonino@email.com.',
        'faq_q14': 'Paano ko makukuha ang aking Barangay Clearance, Certificate of Indigency, o Proof of Residency?',
        'faq_a14': 'Kapag na-aprubahan na ang iyong request, makakatanggap ka ng notification. Magdala ng valid ID at Reference Number sa Barangay Hall para kunin ang iyong dokumento.',
        'faq_q15': 'Saan ko mahahanap ang aking Reference Number?',
        'faq_a15': 'Ang iyong Reference Number ay makikita agad pagkatapos mong magsumite ng request, at makikita rin ito sa pahina ng "Aking mga Request".',
        'faq_q16': 'Paano ako mag-a-apply para sa Event Permit?',
        'faq_a16': 'Pumunta sa "Mag-apply ng Permit" sa sidebar. Punan ang mga detalye ng kaganapan, i-upload ang mga kinakailangang dokumento, at isumite ito nang hindi bababa sa 10 araw bago ang kaganapan.',
        'faq_q17': 'Paano ko masusubaybayan ang status ng aking request o aplikasyon?',
        'faq_a17': 'Pumunta sa pahina ng "Aking mga Request" sa sidebar para makita kung ang iyong request ay Pinoproseso, Aprubado, o Tinanggihan.',
        'faq_q18': 'Saan ako pwedeng mag-check kung available ang venue?',
        'faq_a18': 'Maaari mong tingnan ang "Kalendaryo ng mga Kaganapan" sa sidebar para makita kung ang petsa at lugar na gusto mo ay naka-book na ng ibang event.',
        'faq_q19': 'Saan matatagpuan ang mga available na venue at court?',
        'faq_a19': 'Kabilang sa mga karaniwang venue ang Barangay Covered Court, Multi-Purpose Hall, at mga kalapit na basketball court. Bumisita sa Barangay Hall para sa partikular na reserbasyon.',

        // Request Document Page
        'doc_title': 'Form ng Document Request',
        'doc_subtitle': 'Mag-submit ng request para sa mga dokumento ng barangay',
        'doc_type': 'Uri ng Dokumento',
        'select_doc': 'Pumili ng Uri ng Dokumento',
        'personal_info': 'Personal na Impormasyon',
        'surname': 'Apelyido',
        'given_name': 'Pangalan',
        'middle_name': 'Gitnang Pangalan',
        'address_label': 'Tirahan',
        'phone_label': 'Numero ng Telepono',
        'civil_status': 'Katayuang Sibil',
        'age': 'Edad',
        'dob': 'Petsa ng Kapanganakan',
        'precinct': 'Numero ng Presinto',
        'pob': 'Lugar ng Kapanganakan',
        'length_stay': 'Tagal ng Paninirahan sa Barangay',
        'residency': 'Uri ng Paninirahan',
        'owner': 'May-ari',
        'renter': 'Umuupa',
        'sharer': 'Nakikitira',
        'property_deed': 'Pangalan sa Titulo ng Ari-arian',
        'owner_address': 'Tirahan ng May-ari',
        'family_info': 'Impormasyon ng Pamilya',
        'father': 'Pangalan ng Ama',
        'mother': 'Pangalan ng Ina',
        'spouse': 'Pangalan ng Asawa',
        'occupation': 'Trabaho',
        'emergency': 'KUNG MAY EMERGENCY',
        'emergency_no': 'NUMERO NG TATAWAGAN',
        'ref_person': 'Reference Person',
        'ref1_name': 'Reference 1 - Pangalan',
        'ref1_address': 'Reference 1 - Tirahan',
        'ref2_name': 'Reference 2 - Pangalan',
        'ref2_address': 'Reference 2 - Tirahan',
        'purpose_sig': 'Layunin at Lagda',
        'purpose_doc': 'Layunin ng Pagkuha ng Dokumento',
        'printed_name': 'Nakalimbag na Pangalan (Digital Signature)',
        'date': 'Petsa',
        'terms': 'Mga Tuntunin at Kundisyon',
        'submit_req': 'I-submit ang Request',
        'clear_form': 'Burahin ang Form',
        'area_rep_section': 'Lagda ng Area Representative',
        'select_rep_position': 'Pumili ng Posisyon ng Area Representative',
        'upload_signature': 'Mag-upload ng Lagda ng Area Representative',
        'signature_note': 'Mangyaring mag-upload ng malinaw na lagda ng Area Representative sa itaas ng nakalimbag na pangalan nito kasama ang petsa ng paglagda sa ibaba.',
        'digital_signature_consent': 'Sa pagta-type ng aking nakalimbag na pangalan sa itaas, kinikilala ko na ito ay nagsisilbing aking digital signature, at sumasang-ayon ako sa mga tuntunin at kundisyon na nakasaad sa document request na ito.',
        'data_privacy_consent': 'Ibinibigay ko ang aking informed consent para sa Barangay Sto. Niño na kolektahin, iimbak, at iproseso ang aking personal na impormasyon alinsunod sa Data Privacy Act of 2012 (RA 10173) para sa layunin ng pagproseso ng aking document request.',
        'important_complete_fields': 'Mahalaga: Punan ang Lahat ng Kinakailangang Field',
        'complete_fields_desc': 'Siguraduhing punan ang lahat ng impormasyong may markang * at i-upload ang kinakailangang lagda bago isumite.',
        
        // Apply Permit Page
        'permit_title': 'Aplikasyon ng Permit sa Kaganapan',
        'permit_subtitle': 'Mag-submit ng aplikasyon para sa permit ng kaganapan',
        'event_info': 'Impormasyon ng Kaganapan',
        'event_name': 'Pangalan ng Kaganapan',
        'event_desc': 'Paglalarawan ng Kaganapan',
        'date_time': 'Petsa at Oras',
        'event_date': 'Petsa ng Kaganapan',
        'start_time': 'Oras ng Simula',
        'end_time': 'Oras ng Pagtatapos',
        'venue_attendees': 'Lugar at mga Dadalo',
        'venue': 'Lugar',
        'attendees': 'Inaasahang Dadalo',
        'purpose': 'Layunin',
        'purpose_event': 'Layunin ng Kaganapan',
        'contact_person': 'Taong Kokontakin',
        'contact_phone': 'Telepono ng Contact',
        'supporting_doc': 'Sumusuportang Dokumento',
        'submit_app': 'I-submit ang Aplikasyon',
        'apply_10_days': 'Mahalaga: Mag-apply 10 Araw Bago ang Kaganapan',
        'apply_10_days_desc': 'Mangyaring i-submit ang iyong aplikasyon nang hindi bababa sa 10 araw bago ang petsa ng kaganapan upang bigyang-daan ang tamang pagproseso at pagsusuri ng Barangay staff.',
        'allowed_hours': 'Pinapayagan: 8:00 AM – 10:00 PM lamang',
        'max_attendees': 'Maximum na 300 dadalo',
        'accepted_formats': 'Tinatanggap na format: JPG, PNG, PDF, DOC, DOCX (Max 5MB)',
        'agree_terms': 'Nabasa at sumasang-ayon ako sa Mga Tuntunin at Kundisyon',
        
        // My Requests Page
        'myreq_title': 'Aking mga Request',
        'myreq_subtitle': 'Tingnan ang status ng iyong mga requests at permit',
        'doc_requests': 'Mga Document Request',
        'event_permits': 'Mga Event Permit',
        'doc_requests_list': 'Listahan ng Document Request',
        'event_permits_list': 'Listahan ng Event Permit',
        'total_docs': 'Kabuuang Dokumento',
        'total_permits': 'Kabuuang Permit',
        'pending': 'Kasalukuyang Pinoproseso',
        'approved': 'Aprubado',
        'rejected': 'Tinanggihan',
        'view': 'Tingnan',
        'no_doc_requests': 'Walang Document Request',
        'no_doc_requests_desc': 'Wala ka pang naisumiteng document request.',
        'no_event_permits': 'Walang Event Permit',
        'no_event_permits_desc': 'Wala ka pang naisumiteng event permit application.',
        'document_details': 'Detalye ng Dokumento',
        'event_permit_details': 'Detalye ng Event Permit',
        'reference_no': 'Reference No',
        'date_requested': 'Petsa ng Request',
        'notes': 'Mga Tala',
        'status': 'Status',
        'event_time': 'Oras ng Kaganapan',
        'description': 'Paglalarawan',
        
        // Events Page
        'events_title': 'Kalendaryo ng mga Kaganapan',
        'events_subtitle': 'Pindutin ang petsa para makita ang detalye ng kaganapan',
        'event_details': 'Detalye ng Kaganapan',
        'loading_events': 'Naglo-load ng mga kaganapan...',
        'no_events': 'Walang Kaganapan',
        'events_on_this_date': 'Mga Kaganapan sa Petsang Ito',
        'no_date_selected': 'Walang Napiling Petsa',
        'click_date_details': 'Pindutin ang petsa na may kaganapan upang makita ang detalye dito.',
        'no_approved_events': 'Walang aprubadong kaganapan sa petsang ito.',
        'time_not_specified': 'Oras ay hindi tinukoy',
        'time_label': 'Oras:',
        'venue_label': 'Lugar:',
        'expected_attendees_label': 'Inaasahang Dadalo:',
        
        // Settings Page
        'settings_title': 'Settings',
        'settings_subtitle': 'Pamahalaan ang iyong account at system settings',
        'update_profile': 'I-update ang Profile',
        'update_profile_desc': 'I-update ang iyong personal na impormasyon kabilang ang pangalan, email, at contact details.',
        'change_pass': 'Palitan ang Password',
        'change_pass_desc': 'Palitan ang password ng iyong account para sa mas mahusay na seguridad. Gumamit ng matibay na password.',
        'first_name': 'Pangalan',
        'last_name': 'Apelyido',
        'email_address': 'Email Address',
        'contact_number': 'Numero ng Telepono',
        'address_label_settings': 'Tirahan',
        'cancel': 'Kansel',
        'save_changes': 'I-save ang mga Pagbabago',
        'current_password': 'Kasalukuyang Password',
        'new_password': 'Bagong Password',
        'confirm_new_password': 'Kumpirmahin ang Bagong Password',
        'update_password': 'I-update ang Password',
        
        // Announcements Page
        'announcements_title': 'Mga Anunsyo',
        'announcements_subtitle': 'Pinakabagong Update sa Barangay Sto. Niño',
        'recent_announcements': 'Mga Kamakailang Anunsyo',
        'mark_all_as_read': 'Markahan lahat bilang nabasa',
        'mark_all_as_unread': 'Markahan lahat bilang hindi pa nabasa',
        'view_all_announcements': 'Tingnan Lahat ng Anunsyo',
        'pinned': 'Naka-pin',
        'no_announcements': 'Wala Pang Anunsyo',
        'no_announcements_desc': 'Wala pang announcement na na-post.',

                // Dagdag para sa Notification Panel
        'recent_announcements': 'Mga Kamakailang Anunsyo',
        'mark_all': 'Markahan lahat',
        'no_recent_announcements': 'Walang kamakailang anunsyo',
        'loading': 'Naglo-load...',
        'all_read': 'Nabasa na lahat',

        // Role
        'resident': 'Residente',

        // Form Placeholders & Modal Texts
        'select_doc_placeholder': '-- Pumili ng Uri ng Dokumento --',
        'surname_placeholder': 'Apelyido',
        'given_name_placeholder': 'Pangalan',
        'middle_name_placeholder': 'Gitnang Pangalan',
        'complete_address_placeholder': 'Kumpletong Tirahan',
        'phone_placeholder': '09XXXXXXXXX',
        'age_placeholder': 'Edad',
        'precinct_placeholder': 'Numero ng Presinto',
        'pob_placeholder': 'Lugar ng Kapanganakan',
        'length_stay_placeholder': 'hal. 5 taon',
        'occupation_placeholder': 'Trabaho',
        'property_deed_placeholder': 'Pangalan sa Titulo ng Ari-arian',
        'owner_address_placeholder': 'Tirahan ng May-ari',
        'select_date_placeholder': 'Pumili ng petsa...',
        'select_venue_placeholder': 'Pumili ng lugar...',
        'attendees_placeholder': 'hal., 100',
        'event_name_placeholder': 'hal., Barangay Basketball League',
        'event_desc_placeholder': 'Ilarawan nang maikli ang kaganapan...',
        'event_purpose_placeholder': 'Ilarawan ang layunin ng kaganapan...',
        'time_allowed_note': 'Pinapayagan: 8:00 AM – 10:00 PM lamang',
        'max_attendees_note': 'Maximum na 300 dadalo',
        'select': 'Pumili',
        'cancel_request_title': 'Kanselahin ang Request?',
        'cancel_request_desc': 'Sigurado ka bang gusto mong kanselahin ang request na ito?',
        'cancel_request_warning': 'Ang aksyong ito ay hindi na maibabalik.',
        'no_keep_it': 'Hindi, Itago',
        'yes_cancel': 'Oo, Kanselahin',
        
        // Bagong dagdag base sa screenshot
        'ref_name_placeholder': 'Pangalan ng Reference',
        'ref_address_placeholder': 'Tirahan ng Reference',
        'purpose_req_placeholder': 'Isulat ang layunin ng iyong request...',
        'type_full_name_placeholder': 'I-type ang iyong buong pangalan dito',
        'signature_consent_text': 'Sa pagta-type ng aking nakalimbag na pangalan sa itaas, kinikilala ko na ito ay nagsisilbing aking digital signature, at sumasang-ayon ako sa mga tuntunin at kundisyon na nakasaad sa document request na ito.',
        'privacy_consent_text': 'Ibinibigay ko ang aking informed consent para sa Barangay Sto. Niño na kolektahin, iimbak, at iproseso ang aking personal na impormasyon alinsunod sa Data Privacy Act of 2012 (RA 10173) para sa layunin ng pagproseso ng aking document request.',
        'not_related_to_you': '(Hindi Ka Kaugnay)',
        'by_typing_consent_part1': 'Sa pagta-type ng aking nakalimbag na pangalan sa itaas, kinikilala ko na ito ay nagsisilbing aking',
        'by_typing_consent_part2': 'digital signature',
        'by_typing_consent_part3': ', at sumasang-ayon ako sa mga tuntunin at kundisyon na nakasaad sa document request na ito.',
        'privacy_consent_part1': 'Ibinibigay ko ang aking',
        'privacy_consent_part2': 'informed consent',
        'privacy_consent_part3': 'para sa Barangay Sto. Niño na kolektahin, iimbak, at iproseso ang aking personal na impormasyon alinsunod sa',
        'privacy_consent_part4': 'Data Privacy Act of 2012 (RA 10173)',
        'privacy_consent_part5': 'para sa layunin ng pagproseso ng aking document request.',
        'father_name_placeholder': 'Pangalan ng Ama',
        'mother_name_placeholder': 'Pangalan ng Ina',
        'spouse_name_placeholder': 'Pangalan ng Asawa',
        'emergency_name_placeholder': 'Pangalan ng Tatawagan',
        'emergency_no_placeholder': 'Numero ng Tatawagan',

        // Terms and Conditions - Apply Permit
        'tc_acceptance': '1. Pagsang-ayon sa Mga Tuntunin',
        'tc_acceptance_desc': 'Sa pagsumite ng aplikasyong ito, sumasang-ayon ka na sumunod sa lahat ng alituntunin at regulasyon ng barangay patungkol sa mga kaganapan at pagtitipon.',
        'tc_guidelines': '2. Mga Alituntunin sa Kaganapan',
        'tc_guidelines_desc': 'Ang lahat ng kaganapan ay dapat sumunod sa mga sumusunod:',
        'tc_max_attendees': 'Maximum na 300 dadalo bawat kaganapan',
        'tc_start_time': 'Oras ng Simula: 8:00 AM - 10:00 PM',
        'tc_end_time': 'Oras ng Pagtatapos: 8:00 AM - 10:00 PM',
        'tc_waste': 'Dapat sundin ang tamang pamamahala ng basura',
        'tc_noise': 'Walang sobrang ingay na lalabag sa limitasyon ng barangay',
        'tc_10_days': 'Ang kaganapan ay dapat 10 araw bago ang Petsa ng Kaganapan',
        'tc_responsibility': '3. Responsibilidad',
        'tc_responsibility_desc': 'Ang aplikante ay buong responsibilidad para sa kaganapan at dapat tiyakin ang kaligtasan at kaayusan ng aktibidad.',
        'tc_data_privacy': '4. Data Privacy',
        'tc_data_privacy_desc': 'Ang iyong impormasyon ay gagamitin lamang para sa pagproseso ng permit at mga rekord ng barangay alinsunod sa Data Privacy Act.',
        'tc_cancellation': '5. Patakaran sa Pagkansela',
        'tc_cancellation_desc': 'Ang permit ay dapat kanselahin nang hindi bababa sa 3 araw bago ang kaganapan. Ang kabiguang gawin ito ay maaaring magresulta sa mga parusa.',
        'tc_checkbox_text': 'Nabasa at sumasang-ayon ako sa Mga Tuntunin at Kundisyon ng Barangay Sto. Niño',
        'choose_file': 'Pumili ng File',
        'no_file_chosen': 'Walang napiling file',
        'upload_file_text': 'Pumili ng File',

        // Calendar Days & Menu (Pabuo na base sa request mo)
        'sun': 'LINGGO',
        'mon': 'LUNES',
        'tue': 'MARTES',
        'wed': 'MIYERKULES',
        'thu': 'HUWEBES',
        'fri': 'BIYERNES',
        'sat': 'SABADO',
        'english_menu': 'us English',
        'tagalog_menu': 'ph Tagalog',
        'select_date': 'Pumili ng Petsa',
        'cancel_btn': 'KANSELAHIN',

        // Dagdag na Status
        'processing': 'PINOPROSESO',
        'ready_for_pickup': 'MAARI NANG KUNIN',
        'cancelled': 'Kinansela',

        // Settings Modal Extras
        'req_length': 'Hindi bababa sa 8 character',
        'req_upper': 'Hindi bababa sa 1 uppercase letter',
        'req_lower': 'Hindi bababa sa 1 lowercase letter',
        'req_number': 'Hindi bababa sa 1 numero',
        'req_special': 'Hindi bababa sa 1 special character (!@#$%^&*)',
        'reenter_password': 'Ilagay muli ang bagong password',
        'verify_update': 'I-verify ang Update',
        'enter_code_sent': 'Ilagay ang code na ipinadala sa iyong email',
        'six_digit_code': '6-Digit na Code',
        'verify_save': 'I-verify at I-save',
        'invalid_code': 'Maling code. Pakisubukang muli.',
        'check_email_spam': 'Tingnan ang iyong email inbox (at spam folder).',
        'a_6_digit_code_sent': 'Isang 6-digit na reset code ang ipinadala sa iyong email. Tingnan ang iyong inbox (at spam folder).',
        'password_changed': 'Nabago ang Password!',
        'password_changed_desc': 'Matagumpay na na-update ang iyong password. Isang confirmation email ang ipinadala.',
        'okay_got_it': 'Okay, Nakuha ko',
        'success_title': 'Tagumpay!',
        'profile_updated_desc': 'Matagumpay na na-update ang profile! Isang confirmation email ang ipinadala sa iyong inbox.',
        'sending_code': 'Nagpapadala ng Code...',
        'verifying': 'Nagbe-verify...',
        'verify_code': 'I-verify ang Code',

        // Success Modals (Request & Permit)
        'request_submitted': 'Naipasa ang Request!',
        'request_received': 'Natanggap na ang iyong dokumento request',
        'permit_submitted': 'Naipasa ang Permit!',
        'permit_received': 'Natanggap na ang iyong aplikasyon',
        'please_wait': 'Maghintay Lang',
        'request_pending_desc': 'Ang iyong request ay kasalukuyang',
        'request_pending_desc_2': 'Mangyaring maghintay ng 1-2 business days para sa pagproseso.',
        'permit_pending_desc': 'Ang iyong permit ay kasalukuyang',
        'permit_pending_desc_2': 'Mangyaring maghintay ng 24 oras para sa pagsusuri at pag-apruba ng Barangay staff.',
        'show_qr_code': 'Ipakita ang QR code na ito sa Barangay personnel para mas mabilis ang transaksyon.',
        'notification_ready': 'Makakatanggap ka ng notification kapag handa na ang iyong dokumento.',
        'notification_ready_permit': 'Makakatanggap ka ng notification kapag na-update na ang status ng iyong permit.',
        'track_status': 'I-track ang Status',
        'submit_another': 'Mag-submit ng Isa Pa',
        'request_another': 'Mag-request ng Isa Pa',
        'document_label': 'DOKUMENTO:',
        'applicant_label': 'APLIKANTE:',
        'event_label': 'KAGANAPAN:',
        'date_label': 'PETSA:',
        'time_label_modal': 'ORAS:',
        'venue_label_modal': 'LUGAR:',
        'status_label': 'STATUS:',
        'please_save_number': 'Paki-save ang numerong ito para sa pag-track'
    }
};

function applyGlobalTranslation(lang) {
    const dict = globalTranslations[lang] || globalTranslations['en'];
    const englishDict = globalTranslations['en'];
    
    function translateTextNode(node) {
        if (node.nodeType === 3) { // Text node
            let text = node.nodeValue;
            let trimmed = text.trim();
            
            if (!trimmed || /^\d+$/.test(trimmed)) return;
            
            // 1. Direct Match
            for (const [key, enValue] of Object.entries(englishDict)) {
                if (trimmed.toLowerCase() === enValue.toLowerCase() && dict[key]) {
                    node.nodeValue = text.replace(trimmed, dict[key]);
                    return;
                }
            }

            // 2. Advanced Partial Match (Para sa mga pangungusap na may <strong> sa gitna)
            let newText = text;
            let changed = false;
            
            // Ayusin ang pagkakasunod-sunod: Pinakamahabang salita muna para hindi mag-conflict
            const sortedEntries = Object.entries(englishDict).sort((a, b) => b[1].length - a[1].length);
            
            for (const [key, enValue] of sortedEntries) {
                if (dict[key] && enValue.length > 5 && !newText.includes(dict[key])) {
                    const escapedEnValue = enValue.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                    const regex = new RegExp(escapedEnValue, 'gi');
                    if (regex.test(newText)) {
                        newText = newText.replace(regex, dict[key]);
                        changed = true;
                    }
                }
            }
            if (changed) {
                node.nodeValue = newText;
            }
        } else if (node.nodeType === 1) { // Element node
            if (node.tagName === 'SCRIPT' || node.tagName === 'STYLE') return;
            
            // Translate placeholder attributes
            if (node.hasAttribute('placeholder')) {
                let placeholderText = node.getAttribute('placeholder').trim();
                for (const [key, enValue] of Object.entries(englishDict)) {
                    if (placeholderText.toLowerCase() === enValue.toLowerCase() && dict[key]) {
                        node.setAttribute('placeholder', dict[key]);
                        break;
                    }
                }
            }

            // Translate value attributes
            if (node.tagName === 'INPUT' && (node.type === 'submit' || node.type === 'button' || node.type === 'reset')) {
                let valText = node.value.trim();
                for (const [key, enValue] of Object.entries(englishDict)) {
                    if (valText.toLowerCase() === enValue.toLowerCase() && dict[key]) {
                        node.value = dict[key];
                        break;
                    }
                }
            }

            // Translate title attributes
            if (node.hasAttribute('title')) {
                let titleText = node.getAttribute('title').trim();
                for (const [key, enValue] of Object.entries(englishDict)) {
                    if (titleText.toLowerCase() === enValue.toLowerCase() && dict[key]) {
                        node.setAttribute('title', dict[key]);
                        break;
                    }
                }
            }
            
            const dataKey = node.getAttribute('data-translate');
            if (dataKey && dict[dataKey]) {
                node.textContent = dict[dataKey];
                return;
            }
            
            if (node.classList.contains('translatable')) {
                let key = node.getAttribute('data-original-text');
                if (!key) {
                    key = node.textContent.trim();
                    node.setAttribute('data-original-text', key);
                }
                
                let translated = null;
                for (const [dictKey, enValue] of Object.entries(englishDict)) {
                    if (enValue.toLowerCase() === key.toLowerCase() && dict[dictKey]) {
                        translated = dict[dictKey];
                        break;
                    }
                }
                
                if (translated) {
                    node.textContent = translated;
                }
                return;
            }
            
            node.childNodes.forEach(child => translateTextNode(child));
        }
    }
    
    if (document.body) {
        translateTextNode(document.body);
    }
}

// ✅ AUTO-TRANSLATE CALENDAR (Kapag naka-Tagalog)
function translateCalendar() {
    const lang = localStorage.getItem('language') || 'en';
    if (lang !== 'tl') return;

    // 1. I-override ang FullCalendar locale
    if (window.mainCalendar && typeof window.mainCalendar.setOption === 'function') {
        window.mainCalendar.setOption('locale', 'tl');
        window.mainCalendar.setOption('buttonText', {
            today: 'Ngayon',
            month: 'Buwan',
            week: 'Linggo',
            day: 'Araw',
            list: 'Listahan'
        });
    }

    // 2. I-override ang "month title" (e.g., November -> Nobyembre)
    const monthTitle = document.querySelector('.fc-toolbar-title');
    if (monthTitle) {
        const monthsEn = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        const monthsTl = ['Enero', 'Pebrero', 'Marso', 'Abril', 'Mayo', 'Hunyo', 'Hulyo', 'Agosto', 'Setyembre', 'Oktubre', 'Nobyembre', 'Disyembre'];
        
        let currentTitle = monthTitle.textContent;
        monthsEn.forEach((enMonth, index) => {
            if (currentTitle.includes(enMonth)) {
                currentTitle = currentTitle.replace(enMonth, monthsTl[index]);
            }
        });
        monthTitle.textContent = currentTitle;
    }

    // 3. I-override ang mga araw (SUN, MON -> LINGGO, LUNES)
    const dayHeaders = document.querySelectorAll('.fc-col-header-cell-cushion');
    // Pabuo na base sa request mo bro
    const tagalogDays = ['LINGGO', 'LUNES', 'MARTES', 'MIYERKULES', 'HUWEBES', 'BIYERNES', 'SABADO'];
    dayHeaders.forEach((header, index) => {
        header.textContent = tagalogDays[index % 7];
    });
}

// ✅ Para itago ang mga alert box na may English text kapag naka-Tagalog
function hideEnglishAlerts(lang) {
    if (lang === 'tl') {
        const alerts = document.querySelectorAll('.alert, .alert-warning, .bg-yellow-100, [role="alert"]');
        alerts.forEach(alert => {
            if (alert.textContent.includes('Please') || 
                alert.textContent.includes('Make sure') || 
                alert.textContent.includes('Important') || 
                alert.textContent.includes('submit')) {
                alert.style.display = 'none'; 
            }
        });
    }
}

// ✅ Para maging Tagalog ang browser validation popup (Final Fix)
function overrideBrowserValidation(lang) {
    if (lang !== 'tl') return;

    const applyValidation = () => {
        document.querySelectorAll('input, textarea, select').forEach(input => {
            // Skip hidden inputs
            if (input.type === 'hidden') return;

            // Tanggalin muna ang existing listeners para hindi mag-doble
            input.removeEventListener('invalid', handleInvalid);
            input.removeEventListener('input', handleInput);
            input.removeEventListener('change', handleInput);

            // Idagdag ulit
            input.addEventListener('invalid', handleInvalid);
            input.addEventListener('input', handleInput);
            input.addEventListener('change', handleInput);
        });
    };

    function handleInvalid(e) {
        // Dito natin pinapalitan ang default English message
        this.setCustomValidity("Mangyaring punan ang field na ito.");
    }

    function handleInput(e) {
        // Binabalik sa normal para mawala ang error kapag may tinype na
        this.setCustomValidity("");
    }

    // Patakbuhin agad
    applyValidation();

    // Patakbuhin muli after 500ms para sa mga dynamic na input (tulad ng datepicker)
    setTimeout(applyValidation, 500);
}

// ✅ Para maging Tagalog ang File Upload UI
function overrideFileUploadUI(lang) {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.style.opacity = '0';
        input.style.position = 'absolute';
        input.style.zIndex = '-1';
        
        const wrapper = document.createElement('div');
        wrapper.className = 'custom-file-upload-wrapper';
        wrapper.style.display = 'flex';
        wrapper.style.alignItems = 'center';
        wrapper.style.border = '1px solid #ccc';
        wrapper.style.padding = '5px 10px';
        wrapper.style.borderRadius = '5px';
        wrapper.style.cursor = 'pointer';
        wrapper.style.backgroundColor = '#fff';
        wrapper.style.color = '#333';
        wrapper.style.fontSize = '14px';
        wrapper.style.width = '100%';
        wrapper.style.boxSizing = 'border-box';
        
        const chooseBtnText = lang === 'tl' ? 'Pumili ng File' : 'Choose File';
        const noFileText = lang === 'tl' ? 'Walang napiling file' : 'No file chosen';
        
        wrapper.innerHTML = `
            <span style="border: 1px solid #999; padding: 2px 8px; background: #f0f0f0; margin-right: 10px; border-radius: 3px;">${chooseBtnText}</span>
            <span class="file-name-display">${noFileText}</span>
        `;
        
        input.parentNode.insertBefore(wrapper, input);
        
        wrapper.addEventListener('click', () => {
            input.click();
        });
        
        input.addEventListener('change', (e) => {
            const fileNameDisplay = wrapper.querySelector('.file-name-display');
            if (e.target.files.length > 0) {
                fileNameDisplay.textContent = e.target.files[0].name;
            } else {
                fileNameDisplay.textContent = noFileText;
            }
        });
    });
}

function setGlobalLanguage(lang) {
    localStorage.setItem('language', lang);
    location.reload();
}

document.addEventListener('DOMContentLoaded', function() {
    const savedLang = localStorage.getItem('language') || 'en';
    
    const langText = document.getElementById('currentLangText');
    if (langText) {
        langText.textContent = savedLang === 'tl' ? 'Tagalog' : 'English';
    }
    
    if (savedLang === 'tl') {
        applyGlobalTranslation('tl');
        overrideBrowserValidation('tl');
        overrideFileUploadUI('tl');
        hideEnglishAlerts('tl'); 
        
        setTimeout(translateCalendar, 300);
        setTimeout(translateCalendar, 1000); 
    } else {
        overrideFileUploadUI('en');
    }
});