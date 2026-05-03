import traceback
try:
    from app import app, db
    with app.app_context():
        client = app.test_client()
        response = client.get("/")
        if response.status_code == 200:
            print("SUCCESS! UI Rendered HTTP 200")
        else:
            print(f"FAILED! HTTP {response.status_code}")
            print(response.data.decode('utf-8'))
except Exception as e:
    print("CRASHED!")
    traceback.print_exc()
