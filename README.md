# MM..FOOD
This is a collection of restaurant recommendations that have been conveyed at the watercooler at second floor of Life Sciences C building. Live website at https://mmfood.phoenixeffect.me/. The entire website is powered by a loosely validated but very (human) readable `data.json` file. The json file is converted to static html by the python script `main.py` and deployed on [cloudflare pages](https://pages.cloudflare.com/). Any new commits to the repository automatically triggers a new build by cloudflare and automatic deployment. 

## Contributing
Make sure you are somewhat familiar with [creating pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request). 

Before adding a reviewer, the reviewer needs to be added to the `reviewers` list and the restaurant that has to be added to the `restaurant` list. The `reviewers`, `restaurants` and `review` lists use the name as keys so make sure there are no typos. Below is an example of a basic `data.json` file. Optionally, you can upload a profile photo for the person (square dimensions) in the static/profile/ directory.

```
{
    "reviewers": [
        {
            "name": "Marky",
            "photo": "marky.jpeg",
            "bio": "Hello I am Bio"
        }
    ],
"restaurants": [
        {
            "name": "MedFresh Grill",
            "tags": ["turkish", "close to campus"]
        }
    ],
    "reviews": [
        {
            "reviewer": "Marky",
            "restaurant": "MedFresh Grill",
            "review": "Good food innit"
        }
    ]
}
