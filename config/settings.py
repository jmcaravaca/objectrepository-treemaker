from dataclasses import dataclass

from secret import UIP_CLIENT_ID, UIP_CLIENT_SECRET

@dataclass
class Settings():
    # UIPApiSecrets
    UIP_CLIENT_ID: str
    UIP_CLIENT_SECRET: str
    UIP_SCOPE: str = "OR.Assets OR.Execution OR.BackgroundTasks OR.Folders OR.Jobs OR.Machines OR.Monitoring OR.Queues OR.Robots OR.Settings OR.Tasks OR.Users OR.Webhooks OR.TestDataQueues"
    UIP_GRANT_TYPE: str = "client_credentials"
    UIP_AUTH_TOKENURL: str = "https://cloud.uipath.com/identity_/connect/token"
    UIP_LOGICAL_NAME: str = "clarkemodet"
    UIP_TENANT: str = "ClarkeModetPreProd"
    UIP_TENANT_PRE: str = "ClarkeModetPreProd"
    UIP_TENANT_PRO: str = "ClarkeModetProd"

settings = Settings(UIP_CLIENT_ID=UIP_CLIENT_ID, UIP_CLIENT_SECRET=UIP_CLIENT_SECRET)
