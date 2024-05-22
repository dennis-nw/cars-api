import click

from app.db.session import session_scope
from app.schemas.users import UserCreateSchema
from app.service.users import fetch_user


@click.command()
@click.option("--email", prompt=True, help="The email address of the new user.")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Password.")
def main(email: str, password: str):
    with session_scope() as session:
        user, created = fetch_user(session=session, user=UserCreateSchema(email=email, password=password), create_if_none=True)
    if created:
        click.echo(f"User with email {user.email} has been created.")
    else:
        click.echo(f"User with email {user.email} already exists.")


if __name__ == "__main__":
    main()
