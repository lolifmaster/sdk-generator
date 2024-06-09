import requests


class APIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def _make_authenticated_request(self, method: str, path: str, params: dict = None):
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.request(method, url, headers=headers, params=params)
        return response

    def Accounts_getCdrArrangementAccounts(self, cdrArrangementId, params=None):
        path = f"/adr/banking/arrangements/{cdrArrangementId}/accounts"
        return self._make_authenticated_request("GET", path, params=params)

    def AccountsBalances_getFilteredBalances(self, cdrArrangementId, params=None):
        path = f"/adr/banking/arrangements/{cdrArrangementId}/accounts/balances"
        return self._make_authenticated_request("GET", path, params=params)

    def AccountsBalance_obtainSingleAccountBalance(
        self, cdrArrangementId, accountId, params=None
    ):
        path = (
            f"/adr/banking/arrangements/{cdrArrangementId}/accounts/{accountId}/balance"
        )
        return self._make_authenticated_request("GET", path, params=params)

    def Accounts_obtainDetail(self, cdrArrangementId, accountId, params=None):
        path = f"/adr/banking/arrangements/{cdrArrangementId}/accounts/{accountId}"
        return self._make_authenticated_request("GET", path, params=params)

    def AccountTransactions_getByAccountIdAndCdrArrangementId(
        self, cdrArrangementId, accountId, params=None
    ):
        path = f"/adr/banking/arrangements/{cdrArrangementId}/accounts/{accountId}/transactions"
        return self._make_authenticated_request("GET", path, params=params)

    def AccountTransactions_obtainDetail(
        self, cdrArrangementId, accountId, transactionId, params=None
    ):
        path = f"/adr/banking/arrangements/{cdrArrangementId}/accounts/{accountId}/transactions/{transactionId}"
        return self._make_authenticated_request("GET", path, params=params)

    def AccountDirectDebits_obtainForAccount(
        self, cdrArrangementId, accountId, params=None
    ):
        path = f"/adr/banking/arrangements/{cdrArrangementId}/accounts/{accountId}/direct-debits"
        return self._make_authenticated_request("GET", path, params=params)

    def AccountsDirectDebits_getBulkDirectDebits(self, cdrArrangementId, params=None):
        path = f"/adr/banking/arrangements/{cdrArrangementId}/accounts/direct-debits"
        return self._make_authenticated_request("GET", path, params=params)

    def AccountPaymentsScheduled_getScheduledPayments(
        self, cdrArrangementId, accountId, params=None
    ):
        path = f"/adr/banking/arrangements/{cdrArrangementId}/accounts/{accountId}/payments/scheduled"
        return self._make_authenticated_request("GET", path, params=params)

    def PaymentsScheduled_bulkGet(self, cdrArrangementId, params=None):
        path = f"/adr/banking/arrangements/{cdrArrangementId}/payments/scheduled"
        return self._make_authenticated_request("GET", path, params=params)

    def Payees_getList(self, cdrArrangementId, params=None):
        path = f"/adr/banking/arrangements/{cdrArrangementId}/payees"
        return self._make_authenticated_request("GET", path, params=params)

    def Payees_getDetail(self, cdrArrangementId, payeeId, params=None):
        path = f"/adr/banking/arrangements/{cdrArrangementId}/payees/{payeeId}"
        return self._make_authenticated_request("GET", path, params=params)

    def UserInfo_getByArrangementId(self, cdrArrangementId, params=None):
        path = f"/adr/common/arrangements/{cdrArrangementId}/userinfo"
        return self._make_authenticated_request("GET", path, params=params)

    def Customers_getCustomerInfo(self, cdrArrangementId, params=None):
        path = f"/adr/common/arrangements/{cdrArrangementId}/customer"
        return self._make_authenticated_request("GET", path, params=params)

    def Customers_obtainDetailedInfo(self, cdrArrangementId, params=None):
        path = f"/adr/common/arrangements/{cdrArrangementId}/customer/detail"
        return self._make_authenticated_request("GET", path, params=params)

    def DataHolderDiscovery_getStatus(self, params=None):
        path = "/adr/discovery/status"
        return self._make_authenticated_request("GET", path, params=params)

    def DataHolderDiscovery_getOutages(self, params=None):
        path = "/adr/discovery/outages"
        return self._make_authenticated_request("GET", path, params=params)
