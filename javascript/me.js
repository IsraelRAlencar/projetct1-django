(async function() {
    console.clear();
    const headers = {
        authorization: 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE4NjU5MzE1LCJpYXQiOjE3MTg2NTU3MTUsImp0aSI6IjQ4ZTVkYmQwMjI3ZjRjYTU4ZTljMjk3NmMyMzRjZjM4IiwidXNlcl9pZCI6MX0.-sYRd1n4kxcOsTLyNv2Z6eXcn8vKwbMZ4ODHluTMc3U'
    };
    const config = {
        method: 'GET',
        headers: headers,
    };
    const response = await fetch(
        'http://127.0.0.1:8000/authors/api/me/',
        config
    );
    
    const json = await response.json();
    console.log('status:', response.status);
    console.log(json);
})();