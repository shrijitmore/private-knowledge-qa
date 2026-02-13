import requests
import sys
import json
from datetime import datetime
from pathlib import Path

class KnowledgeQAAPITester:
    def __init__(self, base_url="https://ask-docs-pro.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.uploaded_doc_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, files=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if endpoint else self.api_url
        headers = {}
        if data and not files:
            headers['Content-Type'] = 'application/json'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                if files:
                    response = requests.post(url, files=files, timeout=60)
                else:
                    response = requests.post(url, json=data, headers=headers, timeout=60)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    resp_json = response.json()
                    print(f"   Response: {json.dumps(resp_json, indent=2)[:200]}...")
                    return success, resp_json
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   Error: {error_detail}")
                except:
                    print(f"   Response text: {response.text[:200]}")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timeout")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_api_root(self):
        """Test API root endpoint"""
        return self.run_test("API Root", "GET", "", 200)

    def test_upload_document(self):
        """Upload test document"""
        test_file_path = "/tmp/test_document.txt"
        if not Path(test_file_path).exists():
            print(f"❌ Test file not found: {test_file_path}")
            return False, {}
        
        with open(test_file_path, 'rb') as f:
            files = {'file': ('test_document.txt', f, 'text/plain')}
            success, response = self.run_test(
                "Upload Document", 
                "POST", 
                "documents/upload", 
                200,
                files=files
            )
            if success and response.get('id'):
                self.uploaded_doc_id = response['id']
                print(f"   Document ID: {self.uploaded_doc_id}")
            return success, response

    def test_list_documents(self):
        """Get list of documents"""
        return self.run_test("List Documents", "GET", "documents/", 200)

    def test_ask_question(self):
        """Ask a question about uploaded documents"""
        question_data = {"question": "What are the inner planets?"}
        success, response = self.run_test(
            "Ask Question", 
            "POST", 
            "qa/ask", 
            200, 
            data=question_data
        )
        if success:
            print(f"   Answer length: {len(response.get('answer', ''))}")
            print(f"   Sources count: {len(response.get('sources', []))}")
        return success, response

    def test_qa_history(self):
        """Get Q&A history"""
        return self.run_test("QA History", "GET", "qa/history", 200)

    def test_health_status(self):
        """Get health status"""
        success, response = self.run_test("Health Status", "GET", "status/health", 200)
        if success:
            services = list(response.keys()) if response else []
            print(f"   Services checked: {services}")
            for service, status in response.items():
                status_val = status.get('status', 'unknown')
                print(f"   {service}: {status_val}")
        return success, response

    def test_delete_document(self):
        """Delete uploaded document"""
        if not self.uploaded_doc_id:
            print("❌ No document ID available for deletion")
            return False, {}
        
        return self.run_test(
            "Delete Document", 
            "DELETE", 
            f"documents/{self.uploaded_doc_id}", 
            200
        )

def main():
    print("🚀 Starting Knowledge Q&A API Tests")
    print("=" * 50)
    
    tester = KnowledgeQAAPITester()
    
    # Test sequence
    test_results = []
    
    # Basic API health
    success, _ = tester.test_api_root()
    test_results.append(("API Root", success))
    
    # Health status
    success, _ = tester.test_health_status()
    test_results.append(("Health Status", success))
    
    # Document operations
    success, _ = tester.test_upload_document()
    test_results.append(("Upload Document", success))
    
    success, _ = tester.test_list_documents()
    test_results.append(("List Documents", success))
    
    # Q&A operations
    success, _ = tester.test_ask_question()
    test_results.append(("Ask Question", success))
    
    success, _ = tester.test_qa_history()
    test_results.append(("QA History", success))
    
    # Cleanup
    success, _ = tester.test_delete_document()
    test_results.append(("Delete Document", success))
    
    # Print final results
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    for test_name, success in test_results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:<20} {status}")
    
    print(f"\nOverall: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    success_rate = (tester.tests_passed / tester.tests_run * 100) if tester.tests_run > 0 else 0
    print(f"Success rate: {success_rate:.1f}%")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())