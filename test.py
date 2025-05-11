import requests

NAME = "Adnan Murad"
REG_NO = "1028"
EMAIL = "adnanmurad220792@acropolis.in"

URL = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"


def get_webhook():
    payload = {
        "name": NAME,
        "regNo": REG_NO,
        "email": EMAIL
    }
    try:
        response = requests.post(URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['webhook'], data['accessToken']
    except Exception as e:
        return None, None


def submit_result(webhook_url, access_token, final_query):
    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }
    body = {
        "finalQuery": final_query
    }
    try:
        response = requests.post(webhook_url, headers=headers, json=body)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to submit query: {e}")


def main():
    webhook_url, access_token = get_webhook()
    if not webhook_url or not access_token:
        return

    print(webhook_url, access_token)
    final_query = """
        SELECT 
            EMP1.EMP_ID,
            EMP1.FIRST_NAME,
            EMP1.LAST_NAME,
            DEP.DEPARTMENT_NAME,
            COUNT(EMP2.EMP_ID) AS YOUNGER_EMPLOYEES_COUNT
        FROM 
            EMPLOYEE EMP1
        JOIN 
            DEPARTMENT DEP ON EMP1.DEPARTMENT = DEP.DEPARTMENT_ID
        LEFT JOIN 
            EMPLOYEE EMP2 
            ON EMP1.DEPARTMENT = EMP2.DEPARTMENT
            AND EMP2.DOB > EMP1.DOB
        GROUP BY 
            EMP1.EMP_ID, EMP1.FIRST_NAME, EMP1.LAST_NAME, DEP.DEPARTMENT_NAME
        ORDER BY 
            EMP1.EMP_ID DESC;
    """

    submit_result(webhook_url, access_token, final_query)


if __name__ == "__main__":
    main()
