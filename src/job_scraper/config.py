from dataclasses import dataclass, field

@dataclass
class LinkedIn_Config():
    
    # login credentials 
    mail : str = "......."
    password : str = '.......'

    # URLs
    main_url : str = 'https://www.linkedin.com'
    feed_url : str = 'https://www.linkedin.com/feed/'
    ML_url : str = r"https://www.linkedin.com/jobs/search/?distance=25.0&f_E=2&f_TPR=r86400&f_WT=2&geoId=92000000&keywords=machine%20learning&origin=JOB_SEARCH_PAGE_JOB_FILTER"
    login_url : str = "https://www.linkedin.com/login"
    job_url : str = "https://www.linkedin.com/jobs/search/?currentJobId="

    #Prefrences 
    blacklisted_companies : list = field(default_factory = lambda : ["Kreativstorm", "Refonte Learning AI", "Refonte Learning",
                                                                     "TransPerfect", "Peroptyx", "TELUS International AI Data Solutions", 
                                                                     "Turing",  "Varsity Tutors, a Nerdy Company" ])
    blacklisted_countries: list = field(default_factory = lambda :[])

    # selectors
    next_button_selector : str = 'button[aria-label="View next page"]'  # CSS SELECTOR
    login_button_selector : str = '//button[@type="submit"]'  # XPATH
    page_is_loaded_selector : str = "#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__list > header > div.jobs-search-results-list__title-heading > small > div > span"  # CSS SELECTOR
    jobs_selector : str = "scaffold-layout__list-container" # CLASS NAME
    company_name_selector : str = "#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details > div > div.jobs-search__job-details--container > div > div:nth-child(1) > div > div:nth-child(1) > div > div.relative.job-details-jobs-unified-top-card__container--two-pane > div > div.display-flex.align-items-center > div.display-flex.align-items-center.flex-1 > div" # CSS SELECTOR
    job_title_selector : str = "#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details > div > div.jobs-search__job-details--container > div > div:nth-child(1) > div > div:nth-child(1) > div > div.relative.job-details-jobs-unified-top-card__container--two-pane > div > div.display-flex.justify-space-between.flex-wrap.mt2 > div > h1" # CSS SELECTOR 
    location_selector : str = '#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details > div > div.jobs-search__job-details--container > div > div:nth-child(1) > div > div:nth-child(1) > div > div.relative.job-details-jobs-unified-top-card__container--two-pane > div > div.job-details-jobs-unified-top-card__primary-description-container' # CSS SELECTOR
    job_type_selector : str = "#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details > div > div.jobs-search__job-details--container > div > div:nth-child(1) > div > div:nth-child(1) > div > div.relative.job-details-jobs-unified-top-card__container--two-pane > div > div.mt2.mb2 > ul > li:nth-child(1)"   # CSS SELECTOR


@dataclass
class GlassDoor_Config():

    #URLs
    main_url : str = "https://www.glassdoor.com"
    ML_url : str = "https://www.glassdoor.com/Job/remote-us-machine-learning-jobs-SRCH_IL.0,9_IS11047_KO10,26.htm?remoteWorkType=1&fromAge=1&seniorityType=entrylevel"

    #Prefrences 
    blacklisted_companies : list = field(default_factory = lambda : ["Kreativstorm", "Refonte Learning AI", "Refonte Learning",
                                                                     "TransPerfect", "Peroptyx", "Peroptyx",
                                                                    "TELUS International AI Data Solutions", "Turing"])
    
    # selectors
    mail_selector : str = "#InlineLoginModule > div > div.view-container.inlineInnerContainer.mx-auto.my-0 > div.next > div > div > div > form > div.email-input > div > div.TextInputWrapper"
    go_to_password_selector : str = "#InlineLoginModule > div > div.view-container.inlineInnerContainer.mx-auto.my-0 > div.next > div > div > div > form > div.emailButton > button"
    jobs_list_selector  : str = "#left-column > div.JobsList_wrapper__EyUF6 > ul"


@dataclass
class Indeed_Config():

    #URLs
    main_url : str = "https://www.indeed.com"
    ML_url : str = r"https://www.indeed.com/jobs?q=machine+learning&l=Remote&sc=0kf%3Aattr%28DSQF7%29explvl%28ENTRY_LEVEL%29%3B&rbl=Remote&jlid=aaa2b906602aa8f5&fromage=1&vjk=8f518db1e4deaf19"

    # selectors
    jobs_div_selector : str = "#jobsearch-JapanPage > div > div.css-hyhnne.e37uo190 > div > div.css-pprl14.eu4oa1w0"
