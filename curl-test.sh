#!/bin/bash

# curl-test.sh - Test script for Flask Timeline API endpoints
# Tests POST, GET, and DELETE functionality with random data

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# API base URL
BASE_URL="http://127.0.0.1:5000/api/timeline_post"

CREATED_POST_ID=""

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "INFO")
            echo -e "${BLUE}[INFO]${NC} $message"
            ;;
        "SUCCESS")
            echo -e "${GREEN}[SUCCESS]${NC} $message"
            ;;
        "ERROR")
            echo -e "${RED}[ERROR]${NC} $message"
            ;;
        "WARNING")
            echo -e "${YELLOW}[WARNING]${NC} $message"
            ;;
    esac
}

# Function to generate random test data
generate_random_post() {
    local names=("Alice Johnson" "Bob Smith" "Charlie Brown" "Diana Prince" "Eve Adams" "Frank Miller" "Grace Lee" "Henry Wilson")
    local domains=("gmail.com" "yahoo.com" "outlook.com" "test.edu" "company.org")
    local contents=(
        "Testing the timeline API with automated script!"
        "This is a randomly generated test post."
        "Checking if the database integration works properly."
        "Curl testing is working great!"
        "Flask API endpoint validation in progress."
        "Random test content for timeline post validation."
        "Automated testing makes development easier!"
        "This post was created by the test script."
    )
    
    # Select random elements
    local random_name=${names[$RANDOM % ${#names[@]}]}
    local random_domain=${domains[$RANDOM % ${#domains[@]}]}
    local random_content=${contents[$RANDOM % ${#contents[@]}]}
    
    # Create email from name and domain
    local first_name=$(echo $random_name | cut -d' ' -f1 | tr '[:upper:]' '[:lower:]')
    local last_name=$(echo $random_name | cut -d' ' -f2 | tr '[:upper:]' '[:lower:]')
    local email="${first_name}.${last_name}@${random_domain}"
    
    echo "$random_name|$email|$random_content"
}

# Function to test server availability
test_server() {
    print_status "INFO" "Testing server availability..."
    
    if curl -s --connect-timeout 5 "$BASE_URL" > /dev/null 2>&1; then
        print_status "SUCCESS" "Server is running and accessible"
        return 0
    else
        print_status "ERROR" "Server is not accessible at $BASE_URL"
        print_status "ERROR" "Make sure Flask app is running: flask run"
        return 1
    fi
}

# Function to test GET endpoint (get all posts)
test_get_all() {
    print_status "INFO" "Testing GET endpoint - retrieving all timeline posts..."
    
    local response=$(curl -s -w "\n%{http_code}" "$BASE_URL")
    local http_code=$(echo "$response" | tail -n 1)
    local body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ]; then
        print_status "SUCCESS" "GET request successful (HTTP $http_code)"
        local post_count=$(echo "$body" | jq '.timeline_posts | length' 2>/dev/null)
        if [ $? -eq 0 ]; then
            print_status "INFO" "Current number of posts: $post_count"
        else
            print_status "WARNING" "Could not parse JSON response (jq not installed?)"
        fi
        echo "$body"
        return 0
    else
        print_status "ERROR" "GET request failed (HTTP $http_code)"
        echo "$body"
        return 1
    fi
}

# Function to test POST endpoint (create new post)
test_post() {
    local test_data=$1
    IFS='|' read -r name email content <<< "$test_data"
    
    print_status "INFO" "Testing POST endpoint - creating new timeline post..."
    print_status "INFO" "Name: $name"
    print_status "INFO" "Email: $email"
    print_status "INFO" "Content: $content"
    
    local response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL" \
        -d "name=$name&email=$email&content=$content")
    
    local http_code=$(echo "$response" | tail -n 1)
    local body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ]; then
        print_status "SUCCESS" "POST request successful (HTTP $http_code)"
        local post_id=$(echo "$body" | jq -r '.id' 2>/dev/null)
        if [ $? -eq 0 ] && [ "$post_id" != "null" ]; then
            print_status "SUCCESS" "New post created with ID: $post_id"
            # Only echo the post_id, nothing else
            CREATED_POST_ID="$post_id"
            return 0
        else
            print_status "WARNING" "Post created but could not extract ID" >&2
            return 1
        fi
    else
        print_status "ERROR" "POST request failed (HTTP $http_code)" >&2
        return 1
    fi
}

# Function to test DELETE endpoint
test_delete() {
    local post_id=$1
    
    if [ -z "$post_id" ]; then
        print_status "ERROR" "No post ID provided for deletion"
        return 1
    fi
    
    print_status "INFO" "Testing DELETE endpoint - deleting post ID: $post_id..."
    
    local response=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL/$post_id")
    local http_code=$(echo "$response" | tail -n 1)
    local body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ]; then
        print_status "SUCCESS" "DELETE request successful (HTTP $http_code)"
        echo "$body"
        return 0
    elif [ "$http_code" = "404" ]; then
        print_status "WARNING" "Post ID $post_id not found (HTTP $http_code)"
        echo "$body"
        return 1
    else
        print_status "ERROR" "DELETE request failed (HTTP $http_code)"
        echo "$body"
        return 1
    fi
}

# Function to verify post was added
verify_post_added() {
    local expected_name=$1
    local expected_email=$2
    
    print_status "INFO" "Verifying post was added to database..."
    
    local response=$(curl -s "$BASE_URL")
    local found=$(echo "$response" | jq --arg name "$expected_name" --arg email "$expected_email" \
        '.timeline_posts[] | select(.name == $name and .email == $email)' 2>/dev/null)
    
    if [ -n "$found" ]; then
        print_status "SUCCESS" "Post verification successful - found in database"
        return 0
    else
        print_status "ERROR" "Post verification failed - not found in database"
        return 1
    fi
}

# Main test execution
main() {
    echo "========================================"
    echo "  Flask Timeline API Test Suite"
    echo "========================================"
    echo
    
    # Test server availability
    if ! test_server; then
        exit 1
    fi
    echo
    
    # Initial GET test
    print_status "INFO" "=== INITIAL STATE TEST ==="
    if ! test_get_all; then
        print_status "ERROR" "Initial GET test failed"
        exit 1
    fi
    echo
    
    # Generate random test data
    test_data=$(generate_random_post)
    IFS='|' read -r test_name test_email test_content <<< "$test_data"
    
    # POST test
    print_status "INFO" "=== POST TEST ==="
    test_post "$test_data"
    if [ $? -ne 0 ]; then
        print_status "ERROR" "POST test failed"
        exit 1
    fi
    echo
    
    # Verification test
    print_status "INFO" "=== VERIFICATION TEST ==="
    if ! verify_post_added "$test_name" "$test_email"; then
        print_status "ERROR" "Verification test failed"
        exit 1
    fi
    echo
    
    # Final GET test
    print_status "INFO" "=== FINAL STATE TEST ==="
    if ! test_get_all; then
        print_status "ERROR" "Final GET test failed"
        exit 1
    fi
    echo

    # DELETE test (cleanup)
    if [ -n "$CREATED_POST_ID" ]; then
        print_status "INFO" "=== DELETE TEST (CLEANUP) ==="
        if test_delete "$CREATED_POST_ID"; then
            print_status "SUCCESS" "Test post cleaned up successfully"
        else
            print_status "WARNING" "Could not clean up test post (ID: $CREATED_POST_ID)"
        fi
        echo
    fi
    
    print_status "SUCCESS" "All tests completed successfully!"
    echo "========================================"
}

# Check if script is being run directly
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main "$@"
fi