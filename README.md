# SI 364 - Fall 2018 - Final Project

### **Description**
The following app is a weather status app.
Without logging in, users can look up the weather status of a zipcode location.
Once logged in, users can do the same, except their searches will be saved to a universal search history.
They can also make a weather set based on all the locations that have already been looked up, which is a group of locations and users can simultaneously compare their weather status. Users can afterhand delete or change the names of these sets in the list of sets.

### **Documentation README Requirements**

- [ ] **Create a `README.md` file for your app that includes the full list of requirements from this page. The ones you have completed should be bolded or checked off. (You bold things in Markdown by using two asterisks, like this: `This text would be bold and this text would not be`) and should include a 1-paragraph (brief OK) description of what your application does and have the routes **


### **Code Requirements**
***Note that many of these requirements of things your application must DO or must INCLUDE go together! Note also that*** ***you should read all of the requirements before making your application plan******.***

- [ ] **Ensure that your `SI364final.py` file has all the setup (`app.config` values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on `http://localhost:5000` (and the other routes you set up). **Your main file must be called** `SI364final.py`**, but of course you may include other files if you need.**

- [ ] **A user should be able to load `http://localhost:5000` and see the first page they ought to see on the application.**

- [ ] **Include navigation in `base.html` with links (using `a href` tags) that lead to every other page in the application that a user should be able to click on. (e.g. in the lecture examples from the Feb 9 lecture, [like this](https://www.dropbox.com/s/hjcls4cfdkqwy84/Screenshot%202018-02-15%2013.26.32.png?dl=0) )**

- [ ] **Ensure that all templates in the application inherit (using template inheritance, with `extends`) from `base.html` and include at least one additional `block`.**

- [ ] **Must use user authentication (which should be based on the code you were provided to do this e.g. in HW4).**

- [ ] **Must have data associated with a user and at least 2 routes besides `logout` that can only be seen by logged-in users.**

- [ ] **At least 3 model classes *besides* the `User` class.**

- [ ] **At least one one:many relationship that works properly built between 2 models.**

- [ ] **At least one many:many relationship that works properly built between 2 models.**

- [ ] **Successfully save data to each table.**

- [ ] **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for) and use it to effect in the application (e.g. won't count if you make a query that has no effect on what you see, what is saved, or anything that happens in the app).**

- [ ] **At least one query of data using an `.all()` method and send the results of that query to a template.**

- [ ] **At least one query of data using a `.filter_by(...` and show the results of that query directly (e.g. by sending the results to a template) or indirectly (e.g. using the results of the query to make a request to an API or save other data to a table).**

- [ ] **At least one helper function that is *not* a `get_or_create` function should be defined and invoked in the application.**

- [ ] I DID ONE - At least two `get_or_create` functions should be defined and invoked in the application (such that information can be saved without being duplicated / encountering errors).

- [ ] **At least one error handler for a 404 error and a corresponding template.**

- [ ] **Include at least 4 template `.html` files in addition to the error handling template files.**

- [ ] **At least one Jinja template for loop and at least two Jinja template conditionals should occur amongst the templates.**

- [ ] **At least one request to a REST API that is based on data submitted in a WTForm OR data accessed in another way online (e.g. scraping with BeautifulSoup that *does* accord with other involved sites' Terms of Service, etc).**

- [ ] **Your application should use data from a REST API or other source such that the application processes the data in some way and saves some information that came from the source *to the database* (in some way).**

- [ ] **At least one WTForm that sends data with a `GET` request to a *new* page.**

- [ ] **At least one WTForm that sends data with a `POST` request to the *same* page. (NOT counting the login or registration forms provided for you in class.)**

- [ ] **At least one WTForm that sends data with a `POST` request to a *new* page. (NOT counting the login or registration forms provided for you in class.)**

- [ ] At least two custom validators for a field in a WTForm, NOT counting the custom validators included in the log in/auth code.

- [ ] **Include at least one way to *update* items saved in the database in the application (like in HW5).**

- [ ] **Include at least one way to *delete* items saved in the database in the application (also like in HW5).**

- [ ] **Include at least one use of `redirect`.**

- [ ] **Include at least two uses of `url_for`. (HINT: Likely you'll need to use this several times, really.)**

- [ ] **Have at least 5 view functions that are not included with the code we have provided. (But you may have more!)**


## Additional Requirements for extra points -- an app with extra functionality!

- [ ] (100 points) Include a use of an AJAX request in your application that accesses and displays useful (for use of your application) data.
- [ ]  (100 points) Create, run, and commit at least one migration. (We'll see this from the files generated and can check the history)
- [ ]  (100 points) Deploy the application to the internet (Heroku) — only counts if it is up when we grade / you can show proof it is up at a URL and tell us what the URL is in the README. (Heroku deployment as we taught you is 100% free so this will not cost anything.)



## **To submit**
- Commit all changes to your git repository. Should include at least the files:
  - `README.md`
  - `SI364final.py`
  - A `templates/` directory with all templates you have created inside it
  - May include others (e.g. may include a `static` folder if you are including or uploading static files, but this is not necessary!)
- Create a GitHub account called `364final` on your GitHub account. (You are NOT forking and cloning anything this time, you are creating your own repo from start to finish.)

- Submit the *link* to your GitHub repository to the **SI 364 Final Project** assignment on our Canvas site. The link should be of the form: `https://github.com/YOURGITHUBUSERNAME/364final` (if it doesn't look like that, you are probably linking to something specific *inside* the repo, so make sure it does look like that). You can include your API key separately in the text entry.

All set!
