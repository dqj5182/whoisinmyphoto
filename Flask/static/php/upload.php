<?php
if(isset($_POST['upload']))
{
    $foldername="uploaded_folder";
    mkdir($foldername);
    foreach($_FILES['files']['name'] as $i => $name)
    {
        if(strlen($_FILES['files']['name'][$i]) > 1)
        {move_uploaded_file($_FILES['files']['tmp_name'][$i],$foldername."/".$name);
        }
    }
    echo "Folder is successfully uploaded";

}
?>