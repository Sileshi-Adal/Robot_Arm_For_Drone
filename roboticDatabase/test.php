<?php
      if(isset($_POST['submit']))
      {		try
			{
                $pdo = new PDO(
						'mysql:host=localhost;dbname=test', 'username', 'A6qWGEALrogAgMc4'
				);
				$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
				$pdo->exec('SET NAMES "utf8"');
			}
			catch (PDOException $e)
			{
				$error = 'Unable to connect with the database.';
				include 'output.html.php';
				exit();
			}


// insert the publication into the publication table
            try
            {
                $orderValue = $_POST['order'];
  
                $sql = ("INSERT INTO test (setOrder)
							VALUES ('$orderValue')");
            }catch (\Exception $e)
            {
                echo $e->getMessage();
            }
            try
            {
                $pdo->exec('BEGIN');
                    $pdo->exec($sql);
                $pdo->exec('COMMIT');
            } catch (\Exception $e)
            {
                echo $e->getMessage();
            }
    }
?>