# Doubtnut 

**Endpoints**

- /build_pdf
This endpoint is used to generate dynamic pdfs according to the provided PDF template and data in the request.

Sample body:
```json
{
    "data": [{
        "text": "In math questions answers each questions are solved with explanation. The questions are based from different topics. Care has been taken to solve the questions in such a way that students can understand each and every step.",
        "images": [
            "https://res.cloudinary.com/rahulyadav179023/image/upload/v1590879490/Screenshot_2020-05-31_at_2.52.28_AM_npfshj.png"
        ],
        "videos": [
            "https://ibb.co/CWj05V3",
            "https://ibb.co/CWj05V3",
            "https://ibb.co/CWj05V3"
        ]
    }],
    "pdf_type": "related_questions"
}
```
Sample curl

```
curl --location --request GET 'https://shrouded-scrubland-11934.herokuapp.com/build_pdf' \
--header 'Content-Type: application/json' \
--data-raw '{
    "data": [
        {
            "text": "In math questions answers each questions are solved with explanation. The questions are based from different topics. Care has been taken to solve the questions in such a way that students can understand each and every step.",
            "images": [
                "https://res.cloudinary.com/rahulyadav179023/image/upload/v1590879490/Screenshot_2020-05-31_at_2.52.28_AM_npfshj.png"
            ],
            "videos": [
                "https://ibb.co/CWj05V3",
                "https://ibb.co/CWj05V3",
                "https://ibb.co/CWj05V3"
            ]
        },
        {
            "text": "In math questions answers each questions are solved with explanation. The questions are based from different topics. Care has been taken to solve the questions in such a way that students can understand each and every step.",
            "images": [
                "https://res.cloudinary.com/rahulyadav179023/image/upload/v1590879490/Screenshot_2020-05-31_at_2.52.28_AM_npfshj.png"
            ],
            "videos": [
                "https://ibb.co/CWj05V3",
                "https://ibb.co/CWj05V3",
                "https://ibb.co/CWj05V3"
            ]
        },
        {
            "text": "In math questions answers each questions are solved with explanation. The questions are based from different topics. Care has been taken to solve the questions in such a way that students can understand each and every step.",
            "images": [
                "https://res.cloudinary.com/rahulyadav179023/image/upload/v1590879490/Screenshot_2020-05-31_at_2.52.28_AM_npfshj.png"
            ],
            "videos": [
                "https://ibb.co/CWj05V3",
                "https://ibb.co/CWj05V3",
                "https://ibb.co/CWj05V3"
            ]
        }
    ],
    "pdf_type": "related_questions"
}'
```

**Local development Steps**
```
docker build -f Dockerfile-dev . -t local_dobtnut
docker run  --env PORT=5000 --env DEBUG=True -p 5000:5000 -v $(PWD):/code local_dobtnut (the sever will reload on file changes)
```

**Deployment on prod with heroku**  (no access to k8's cluster) 

I'm assuming you have created an app on heroku and pushed code
in mater branch
```
heroku container:push web (builds and pushes multistage Dockerfile used for prod)
heroku container:release web

```
API is currenlt deplyed at [URL](https://shrouded-scrubland-11934.herokuapp.com/build)
The first request can take about 10-12 seconds since the deployment scales dynamicalaly where min pod is set to zero at the moment (for free accounts). When the first request comes in the service is deployed and post that, requests will have usual api response time.

**Some Caveats**

I have used pdfkit package in python for converting HTML in to pdf which internally uses Wkhtmltopdf. Wkhtmltopdf's debian  package has major issues like patched qt-version due to which custom things are done both in dockerfile and code


**Improvements  (Did not complete due to time constraints)**

+ Replacing flask dev server with gunicorn
+ Add tests for the api
+ Better templating
+ Focus on Design of the PDF generated
+ Directory Strucuture
