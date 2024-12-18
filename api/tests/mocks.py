user_stories = [
    {
        "id": "us-123456",
        "session_id": "fcc95c16-28ae-4bc5-bead-cf052ab87cef",
        "title": "User Login and Profile Update",
        "startTimestamp": "2023-09-16T10:30:15Z",
        "endTimestamp": "2023-09-16T10:31:45Z",
        "initialState": {
            "url": "https://example.com/login"
        },
        "actions": [
            {
                "type": "input",
                "target": "#email",
                "value": "user@example.com"
            },
            {
                "type": "input",
                "target": "#password",
                "value": "********"
            },
            {
                "type": "click",
                "target": "#login-button"
            },
            {
                "type": "navigation",
                "url": "https://example.com/profile"
            },
            {
                "type": "input",
                "target": "#display-name",
                "value": "John Doe"
            },
            {
                "type": "click",
                "target": "#save-profile"
            }
        ],
        "networkRequests": [
            {
                "url": "https://api.example.com/login",
                "method": "POST",
                "status": 200
            },
            {
                "url": "https://api.example.com/profile",
                "method": "PUT",
                "status": 200
            }
        ],
        "finalState": {
            "url": "https://example.com/profile",
            "displayName": "John Doe"
        }
    }
]

code = \
"""def test_us-123456(page):
    # Test steps
    page.locator("#email").fill("user@example.com")
    page.locator("#password").fill("********")
    page.locator("#login-button").click()
    page.goto("https://example.com/profile")
    page.locator("#display-name").fill("John Doe")
    page.locator("#save-profile").click()

    # Assertions
    expect(page.url()).to_be("https://example.com/profile")
    expect(page.locator("#display-name")).to_have_text("John Doe")"""