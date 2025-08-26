class API:
    def get_data(self):
        # @accept API to User with "GET request"
        return {"data": "Hello World"}

    def send_data(self):
        # @threat "Information Disclosure" to API with "Sensitive data over HTTP"
        pass

    def secure_data(self):
        # @mitigate API against "Information Disclosure" with "Use HTTPS instead of HTTP"
        pass

class Database:
    def connect(self):
        # @threat "SQL Injection" to Database with "Unsanitized input"
        pass

    def query(self):
        # @mitigate Database against "SQL Injection" with "Use parameterized queries"
        pass

