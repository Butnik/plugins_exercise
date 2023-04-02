from plugin import Plugin
import requests
import json
class DummyApiPlugin(Plugin):
    def __init__(self, base_url, access_token, valid_endpoint, invalid_endpoint, api_url, output_file1, output_file2):
        self.base_url = base_url
        self.access_token = access_token
        self.valid_endpoint = valid_endpoint
        self.invalid_endpoint = invalid_endpoint
        self.api_url = api_url
        self.output_file1 = output_file1
        self.output_file2 = output_file2


    def connectivity_test(self):

        headers = {"Authorization": f"Bearer {self.access_token}"}
        valid_url = self.base_url + self.valid_endpoint
        invalid_url = self.base_url + self.invalid_endpoint
        worksWithValid = False
        worksWithInvalid = False

        try:
            # Test valid endpoint with access token
            response = requests.get(valid_url, headers=headers)
            response.raise_for_status()
            print("API connectivity test successful with valid access token!")
            worksWithValid = True
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                print("API connectivity test failed with invalid access token!")
            else:
                print(f"API connectivity test failed with error {response.status_code}: {e}")

        try:
            # Test invalid endpoint with access token
            response = requests.get(invalid_url, headers=headers)
            response.raise_for_status()
            print("API connectivity test successful with invalid endpoint!")
            worksWithInvalid = True

        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                print("API connectivity test failed with invalid access token!")
            else:
                print(f"API connectivity test successful with error {response.status_code}: {e}")
        except requests.exceptions.RequestException as e:
            print(f"API connectivity test failed with error: {e}")

        return (worksWithValid and not worksWithInvalid)
    def collect(self):
        users = []
        page_num = 1
        while True:
            response = requests.get(f"{self.api_url}?page={page_num}")
            page_users = response.json().get('users', [])
            if not page_users:
                break
            users.extend(page_users)
            page_num += 1
        with open(self.output_file1, 'w') as f:
            json.dump(users, f, default=str)

        posts_with_comments = []
        # Fetch the first 50 posts
        posts_response = requests.get(f"{self.api_url}/posts?_limit=50")
        posts = posts_response.json()

        for post in posts:
            # Fetch comments for each post
            comments_response = requests.get(f"{self.api_url}/comments?postId={post['id']}")
            comments = comments_response.json()

            # Add comments to post dictionary
            post['comments'] = comments

            # Add post with comments to list
            posts_with_comments.append(post)

        # Write posts with comments to file
        with open(self.output_file2, 'w') as f:
            json.dump(posts_with_comments, f)

        return posts_with_comments






