import os
from pathlib import Path
import subprocess

def get_user_input(prompt, default=None, required=True):
    """
    Récupère une entrée utilisateur avec un message personnalisé, 
    un défaut facultatif, et vérifie si la valeur est requise.
    """
    while True:
        user_input = input(f"{prompt} ({'Default: ' + default if default else 'Required'}): ").strip()
        if user_input:
            return user_input
        elif default is not None:
            return default
        elif required:
            print("❌ This field is required. Please provide a value.")
        else:
            return ""

def create_env_file(env_path):
    """
    Crée un fichier .env basé sur les entrées de l'utilisateur.
    """
    print("\n--- Configuration des variables d'environnement ---")
    db_user = get_user_input("Database user (DB_USER)", default="postgres")
    db_password = get_user_input("Database password (DB_PASSWORD)", required=True)
    db_name = get_user_input("Database name (DB_NAME)", required=True)
    db_host = get_user_input("Database host (DB_HOST)", default="db")
    db_port = get_user_input("Database port (DB_PORT)", default="5432")

    env_content = (
        f"DB_USER={db_user}\n"
        f"DB_PASSWORD={db_password}\n"
        f"DB_NAME={db_name}\n"
        f"DB_HOST={db_host}\n"
        f"DB_PORT={db_port}\n"
    )

    with open(env_path, "w") as env_file:
        env_file.write(env_content)
    print(f"✅ Fichier .env créé avec succès à : {env_path}")

def check_docker_compose():
    """
    Vérifie si Docker et Docker Compose sont installés.
    """
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        subprocess.run(["docker-compose", "--version"], check=True, capture_output=True)
        print("✅ Docker et Docker Compose sont installés.")
    except FileNotFoundError as e:
        print("❌ Docker ou Docker Compose n'est pas installé. Veuillez l'installer avant de continuer.")
        exit(1)

def build_and_run_docker():
    """
    Lance la construction et l'exécution avec docker-compose.
    """
    try:
        print("\n--- Lancement de Docker Compose ---")
        subprocess.run(["docker-compose", "up", "--build"], check=True)
    except subprocess.CalledProcessError as e:
        print("❌ Une erreur est survenue lors de l'exécution de Docker Compose.")
        exit(1)

def main():
    """
    Point d'entrée principal du script.
    """
    print("⚙️  Initialisation de la configuration Docker et du fichier .env")
    root_path = Path(__file__).parent
    env_path = root_path / ".env"

    # Création du fichier .env
    create_env_file(env_path)

    # Vérification de Docker et Docker Compose
    check_docker_compose()

    # Lancement de docker-compose
    build_and_run_docker()

if __name__ == "__main__":
    main()