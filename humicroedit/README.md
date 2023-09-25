# Pun Editing Interface

The pun editing interface (in Portuguese) was created using [Streamlit](https://streamlit.io/), using python.

## How to run

To run the interface, you should first install the prerequisites. Using pipev:

```bash
pipenv install
```

Or pip:

```bash
pip install -r requirements.txt
```

Then to run the streamlit server:

```bash
streamlit run ./1_🏠_Início.py
```

## Configuration

The whole authentication and corpus splitting processes are controlled via the `config.yaml` file.

### Authentication

The authentication process is implemented using the [Streamlit Authenticator](https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/) API. The credentials are stored in the `.yaml` file with the following structure:

```yaml
credentials:
  usernames:
    annotator1: # Username
      name: Annotator1 # Annotator name
      password: password1 # Hashed password
    annotator2:
      name: Annotator2
      password: password2
cookie: # Cookies configuration
  expiry_days: 30
  key: humicroedit
  name: humicroedit_authentication
preauthorized: # Required for Streamlit authenticator. Not used
  emails: # Required for Streamlit authenticator. Not used
```

It is easy to add new annotators by including them to the `config.yaml` file.

Remember to hash the passwords using the python API:

```python
import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(['password1', 'password2']).generate()
```

### Corpus splitting

To split the corpus evenly across annotators, we classified each annotator according to their main language variant. We do this with the following configuration schema in `config.yaml`. Similarly, the pun sources are also classified according to their main dialect of Portuguese.

```yaml
countries:
  brazil:
    - annotator1
    - annotator 2
  portugal:
    - annotator 3
sources:
  brazil:
    - 1
    - 2
    - 3
    - 5
  portugal:
    - 4
```

### Managing permissions

Some actions --- namely the preprocessing and splitting of the corpus, and seeing the whole annotation progess --- are restricted to specific users. These should be defined in `config.yaml` as follows:

```yaml
admins:
 - annotator1
 - annotator3
```

