<?php
session_start(); // Démarrer la session

// Connection à la base de données
$host = 'localhost';
$dbname = 'budget_ai';
$username = 'root';
$password = ''; // Changez selon votre configuration

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Erreur de connexion : " . $e->getMessage());
}

// Vérifier les informations d'inscription
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';
    $confirm_password = $_POST['confirm_password'] ?? '';

    if ($password === $confirm_password) {
        // Hacher le mot de passe
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);

        // Insérer l'utilisateur dans la base de données
        $stmt = $pdo->prepare("INSERT INTO users (email, mdp) VALUES (?, ?)");
        $stmt->execute([$email, $hashed_password]);

        // Rediriger vers la page de connexion
        header("Location: connexion.php");
        exit;
    } else {
        echo "Les mots de passe ne correspondent pas.";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bienvenue sur BUDGET AI - Inscription</title>
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
  
          input, select, button {
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
    <h2>Inscription</h2>
    <form method="POST" action="inscription.php">
        <label for="email">Email :</label>
        <input type="email" id="email" name="email" required>
        <br>
        <label for="nom">Nom :</label>
        <input type="text" id="nom" name="nom" required>
        <br>
        <label for="password">Mot de passe :</label>
        <input type="password" id="password" name="password" required>
        <br>
        <label for="confirm_password">Confirmer le mot de passe :</label>
        <input type="password" id="confirm_password" name="confirm_password" required>
        <br>
        <button type="submit">S'inscrire</button>
    </form>
    <form action="connexion.php" method="get"> <button type="submit">Page Connexion</button> </form>
</body>
</html>
