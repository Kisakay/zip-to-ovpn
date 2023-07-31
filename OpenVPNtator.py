import os

def combine_files_to_ovpn_folder(folder_path):
    # Vérifier si le dossier existe
    if not os.path.exists(folder_path):
        print("Le dossier spécifié n'existe pas.")
        return
    
    # Vérifier si tous les fichiers requis existent dans le dossier
    required_files = ['ca.crt', 'client.crt', 'client.key', 'openvpn.ovpn']
    missing_files = [file for file in required_files if not os.path.exists(os.path.join(folder_path, file))]
    if missing_files:
        print("Les fichiers suivants sont manquants dans le dossier :")
        print("\n".join(missing_files))
        return
    
    # Lire le contenu des fichiers
    file_contents = {}
    for file in required_files:
        with open(os.path.join(folder_path, file), 'r') as f:
            file_contents[file] = f.read()

    # Supprimer les lignes mentionnant les fichiers de certificats et de clés
    for key in ['ca ca.crt', 'cert client.crt', 'key client.key']:
        file_contents['openvpn.ovpn'] = file_contents['openvpn.ovpn'].replace(f"{key}\n", "")

    # Créer le fichier combined.ovpn
    combined_ovpn_path = os.path.join(folder_path, 'combined.ovpn')
    with open(combined_ovpn_path, 'w') as combined_ovpn_file:
        combined_ovpn_file.write(file_contents['openvpn.ovpn'])
        combined_ovpn_file.write("<ca>\n")
        combined_ovpn_file.write(file_contents['ca.crt'].replace("ca ca.crt", "ez").strip())
        combined_ovpn_file.write("\n</ca>\n\n<cert>\n")
        combined_ovpn_file.write(file_contents['client.crt'].replace("cert client.crt", "").strip())
        combined_ovpn_file.write("\n</cert>\n\n<key>\n")
        combined_ovpn_file.write(file_contents['client.key'].replace("key client.key", "").strip())
        combined_ovpn_file.write("\n</key>\n\n")
    print(f"Le fichier combined.ovpn a été créé avec succès dans le dossier {folder_path}.")

# Exécution du script en spécifiant le dossier contenant les fichiers
if __name__ == "__main__":
    folder_path = input("Entrez le chemin du dossier contenant les fichiers (ex: /chemin/vers/le/dossier) : ")
    combine_files_to_ovpn_folder(folder_path)
