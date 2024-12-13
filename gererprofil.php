<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gérer le Profil</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
            background-color: #f9f9f9;
        }

        .container {
            max-width: 500px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }

        h2 {
            text-align: center;
            color: #4CAF50;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        label {
            font-weight: bold;
        }

        input, button {
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }

        button {
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }

        .back-link {
            display: block;
            text-align: center;
            margin-top: 10px;
            color: #4CAF50;
            text-decoration: none;
        }

        .back-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>

<?php
session_start();
$id = $_SESSION['user_id'];

// Connexion à la base de données
$host = 'localhost';
$dbname = 'budget_ai';
$username = 'root';
$password = '';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Erreur de connexion à la base de données : " . $e->getMessage());
}

// Vérifier si la requête est POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $id = $_POST['id'] ?? null;
    $nom = $_POST['nom'] ?? '';
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';

    if ($id && $nom && $email && $password) {
        // Hasher le mot de passe
        $hashedPassword = password_hash($password, PASSWORD_DEFAULT);

        // Mettre à jour l'utilisateur
        $stmt = $pdo->prepare("UPDATE users SET nom = ?, email = ?, mdp = ? WHERE id = ?");
        $stmt->execute([$nom, $email, $hashedPassword, $id]);

        // Rediriger avec un message de succès
        header("Location: Acceuil.php");
        exit;
    } else {
        // Gérer les erreurs
        header("Location: gererprofil.php");
        exit;
    }
}
?>

    <div class="container">
        <h2>Gérer le Profil</h2>
        <form action="/update_profile.php" method="POST">
            <!-- Champ masqué pour l'ID -->
            <input type="hidden" id="id" name="id" value="<!-- ID utilisateur ici -->">

            <label for="nom">Nom :</label>
            <input type="text" id="nom" name="nom" placeholder="Entrez votre nom" required>

            <label for="email">Email :</label>
            <input type="email" id="email" name="email" placeholder="Entrez votre email" required>

            <label for="password">Mot de Passe :</label>
            <input type="password" id="password" name="password" placeholder="Entrez un nouveau mot de passe" required>

            <button type="submit">Enregistrer les modifications</button>
        </form>

        <a href="Acceuil.php" class="back-link">Retour à l'accueil</a>
    </div>
</body>
</html>