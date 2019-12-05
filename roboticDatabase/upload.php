<?php
      if(isset($_POST['submit']))
      {		try
			{
                $pdo = new PDO(
						'mysql:host=localhost;dbname=roboticarm', 'eagles', 'UniversityOfTurku'
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
			
			try
			{


// path of the file to be uploaded
//$target_file = $target_dir.basename($_FILES["fileToUpload"]["name"]);
//$target_dir = "D:/Downloads/Opera Downloads/pictures";
				$target_file = $_FILES["uploadImage"]["name"];
				$uploadOk = 1;
//file extension in lower case
				$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
// check if image file is acutal or fake
				if(isset($_POST["submit"]))
				{
					$check = getimagesize($_FILES["uploadImage"]["tmp_name"]);
					if($check !== false) 
					{
						echo "File is an image - " . $check["mime"] . ".";
						$uploadOk = 1;
					}
					else
					{
						echo "File is not an image.";
						echo "Sorry, your file was not uploaded.";
						$uploadOk = 0;
						exit();
					}
				}
// if file is larger than 2MB error message is displayed
				$fileSize = $_FILES["uploadImage"]['size'];
				if($fileSize > 2000000)
				{
					echo "The selected image is larger than 2MB.";
					echo "Sorry, your file was not uploaded.";
					$uploadOk = 0;
					exit();
				}
//upload only JPG, JPEG, PNG & GIF files
				if($imageFileType != "jpg" && $imageFileType != "jpeg" &&
					$imageFileType != "gif" && $imageFileType != "png")
					{
						echo "Invalid file type";
						echo " select only JPG, JPEG, PNG or gif";
						echo "Sorry, your file was not uploaded.";
						$uploadOk = 0;
						exit();
					}

// if everything is ok, try to upload file
				try
				{
					move_uploaded_file($_FILES["uploadImage"]["tmp_name"], $target_file);
				}
				catch(PDOException $e)
				{
					echo "Sorry, there was an error uploading your file.";
					$error = 'Error fetching data.'.$e->getMessage();
					include 'error.html.php';
					exit();
				}
			}
			catch(PDOException $e)
			{
				$error = 'Error fetching data.'.$e->getMessage();
				include 'error.html.php';
				exit();
			}
// insert the publication into the publication table
            try
            {
                echo "<br>";
                $file = fopen($target_file, 'r');
                $content = fread($file, filesize($target_file));
                $content = addslashes($content);
                fclose($file);
				$orderValue = 1;
				$status = "Waiting";

                $sql = ("INSERT INTO task (name, picture, setOrder, size, status)
							VALUES ('$target_file', '$content', '$orderValue', '$fileSize', '$status')");
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
