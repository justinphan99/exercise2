from app.controller.accountController import AccountController, AccountTokenController, AccountTopupController
from app.controller.merchantController import MerchantController, MerchantUpdateOrderController
from app.controller.transactionController import *

routes = {
    "/account" : AccountController(),
    "/merchant/signup": MerchantController(),
    "/account/{accountId}/token": AccountTokenController(),
    "/account/{accountId}/topup": AccountTopupController(),
    "/transaction/create": TransactionCreateController(),
    "/transaction/confirm": TransactionConfirmController(),
    "/transaction/verify": TransactionVerifyController(),
    "/transaction/cancel": TransactionCancelController(),
    "/merchant/update": MerchantUpdateOrderController()
}