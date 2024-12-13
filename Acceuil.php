<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestion des Dépenses</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        header {
            background-color: #4CAF50;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
        }

        header .logo {
            font-size: 24px;
            font-weight: bold;
        }

        header .buttons {
            display: flex;
            gap: 10px;
        }

        header .buttons button {
            background-color: white;
            color: #4CAF50;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
        }

        header .buttons button:hover {
            background-color: #45a049;
            color: white;
        }

        #balance {
            font-size: 18px;
            font-weight: bold;
        }

        .main {
            padding: 20px;
        }

        .section {
            margin-bottom: 30px;
        }

        .table-container {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        table th, table td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }

        table th {
            background-color: #f2f2f2;
        }

        .income {
            color: green;
        }

        .expense {
            color: red;
        }

        .charts {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }

        .chart {
            width: 45%;
            height: 300px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .chatbot {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .chatbot textarea {
            width: 100%;
            height: 100px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }

        .chatbot button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
        }

        .chatbot button:hover {
            background-color: #45a049;
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <?php
    session_start(); // Démarrer la session
     // Vérifier si l'utilisateur est connecté 
     if (!isset($_SESSION['user_id'])) { header("Location: connexion.php"); exit; } 
     // Récupérer l'ID de l'utilisateur 
     $user_id = $_SESSION['user_id'];
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

// Utiliser l'ID de l'utilisateur pour récupérer les données spécifiques 
$stmt = $pdo->prepare("SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC");
 $stmt->execute([$user_id]); 
 $transactions = $stmt->fetchAll(PDO::FETCH_ASSOC);


// Récupérer les transactions
$stmt = $pdo->prepare("SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC"); $stmt->execute([$user_id]); $transactions = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Calculer le solde
$solde = 0;
foreach ($transactions as $transaction) {
    if ($transaction['type'] === 'Revenu') {
        $solde += $transaction['montant'];
    } else {
        $solde -= $transaction['montant'];
    }
}
?>

    <!-- Section 1 -->
    <header>
        <div class="logo">BudgetAI</div>
        <div id="balance">Solde: <?= number_format($solde, 2) ?> MAD</div>
        <div class="buttons">
            
            <form action="connexion.php" method="get"> <button type="submit">Se déconnecter</button> </form>

            <form action="gererprofil.php" method="get"> <button type="submit">Gérer Profil</button> </form>

        
            <form action="ajoutrev.php" method="get"> <button type="submit">Ajouter Transaction</button> </form>
            
        </div>
    </header>

    <div class="main">
        <!-- Section 2 -->
        <div class="section">
            <h2>Tableau des Transactions</h2>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Type</th>
                            <th>Catégorie</th>
                            <th>Montant</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($transactions as $transaction): ?>
                            <tr>
                                
                                <td><?= htmlspecialchars($transaction['type']) ?></td>
                                <td><?= htmlspecialchars($transaction['categorie']) ?></td>
                                <td class="<?= $transaction['type'] === 'Revenu' ? 'income' : 'expense' ?>">
                                    <?= $transaction['type'] === 'Revenu' ? '+' : '-' ?>
                                    <?= number_format($transaction['montant'], 2) ?> MAD
                                </td>
                                
                                <td><?= htmlspecialchars($transaction['date']) ?></td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>

            <div class="charts">
                <div class="chart"> <h2>Proportions des Dépenses par Catégorie</h2>
                <canvas id="pieChart" width="40" height="40"></canvas></div>
                <div class="chart">Diagramme en Camembert</div>
            </div>
        </div>

        <!-- Section 3 -->
        <div class="section chatbot">
            <h2>Conseils Personnalisés</h2>
            <textarea placeholder="Entrez vos questions ou informations ici..."></textarea>
            <button>Demander Conseil</button>
        </div>
    </div>
    <script>
        async function loadPieData() {
            const response = await fetch('get_pie_data.php');
            const data = await response.json();

            const categories = data.map(item => item.categorie);
            const totals = data.map(item => parseFloat(item.total));
            const colors = categories.map(() => `#${Math.floor(Math.random() * 16777215).toString(16)}`);

            const ctx = document.getElementById('pieChart').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: categories,
                    datasets: [{
                        data: totals,
                        backgroundColor: colors,
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'top' },
                        title: { display: true, text: 'Proportions des Dépenses par Catégorie' }
                    }
                }
            });
        }

        window.onload = loadPieData;
    </script>
</body>
</html>
