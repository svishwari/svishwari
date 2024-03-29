"""Module to house the delivery platform (destinations) pre-populate data"""
from huxunifylib.database import constants as db_c

DELIVERY_PLATFORM_LIST = [
    {
        db_c.DELIVERY_PLATFORM_NAME: "Facebook",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_FACEBOOK,
        db_c.LINK: "https://business.facebook.com/",
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.ACTIVE,
        db_c.ENABLED: True,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Google Ads",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_GOOGLE,
        db_c.LINK: "https://ads.google.com/nav/login",
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Salesforce Marketing Cloud",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SFMC,
        db_c.LINK: "https://members.exacttarget.com/Login.aspx?ReturnUrl=%2F",
        db_c.CATEGORY: db_c.MARKETING,
        db_c.STATUS: db_c.ACTIVE,
        db_c.ENABLED: True,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Sendgrid by Twilio",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SENDGRID,
        db_c.LINK: "https://app.sendgrid.com/login",
        db_c.CATEGORY: db_c.MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Qualtrics",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_QUALTRICS,
        db_c.LINK: "https://login.qualtrics.com/login",
        db_c.CATEGORY: db_c.SURVEY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Amazon Advertising",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_AMAZON,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Liveramp",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_LIVERAMP,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Pinterest",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_PINTEREST,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "TheTradeDesk",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_THE_TRADEDESK,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Twitter",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_TWITTER,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Google DV360",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_GOOGLE_DV360,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.ADVERTISING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: True,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Fullstory",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_FULLSTORY,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.ANALYTICS,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "QuantumMetric",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_QUANTUMMETRIC,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.ANALYTICS,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Salesforce Commerce Cloud",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SFCC,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.COMMERCE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "SAP",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SAP,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.COMMERCE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Adobe Campaign",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_ADOBE_CAMPAIGN,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Adobe Experience Platform",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_ADOBE,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Salesforce CDP",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SALESFORCE_CDP,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.MARKETING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Salesforce Datorama",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SALESFORCE_DATORAMA,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.CATEGORY_REPORTING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Tableau",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_TABLEAU,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.CATEGORY_REPORTING,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "AWS S3",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_AMAZONS3,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.CATEGORY_STORAGE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Azure Blob",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_AZUREBLOB,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.CATEGORY_STORAGE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Google Cloud Storage",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_GOOGLE_CLOUD_STORAGE,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.CATEGORY_STORAGE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "SFTP",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SFTP,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.CATEGORY_STORAGE,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
    {
        db_c.DELIVERY_PLATFORM_NAME: "Medallia",
        db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_MEDALLIA,
        db_c.LINK: "",
        db_c.CATEGORY: db_c.SURVEY,
        db_c.STATUS: db_c.PENDING,
        db_c.ENABLED: False,
        db_c.ADDED: False,
        db_c.IS_AD_PLATFORM: False,
    },
]
