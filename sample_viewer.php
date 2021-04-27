  <?php
  function getColorCode($level)
  {
    $redAmount = intval(255 * (1 - $level));
    $greenAmount = intval(255 * $level);
    $blueAmount = 0;
    return "rgb(" . strval($redAmount) . "," . strval($greenAmount) . "," . strval($blueAmount) . ")";
  }
  ?>

  <!DOCTYPE html>
  <html>

  <head>
    <meta charset="utf-8">
    <title>WordInventor Sample Visualizer</title>
  </head>

  <body>

    <style>
      table {
        border-collapse: collapse;
      }

      table th,
      td {
        border: solid black 1px;
      }
    </style>

    <h1>Tableau des fréquences d'enchaînement</h1>


    <table>
      <thead>
        <?php
        $row = 1;
        if (($handle = fopen("sequences_sample.csv", "r")) !== FALSE) {
          if (($data = fgetcsv($handle, 1000, ";")) !== FALSE) {
        ?>
            <tr>
              <?php
              for ($c = 0; $c < count($data); $c++) {
              ?>
                <th style="width: 15px;"><?php echo $data[$c] ?></th>
              <?php
              }
              ?>
            </tr>
        <?php
          }
        }
        ?>
      </thead>

      <tbody>
        <?php
        $row = 1;
        if (($handle = fopen("sequences_sample.csv", "r")) !== FALSE) {
          fgetcsv($handle, 1000, ";"); //skip header
          while (($data = fgetcsv($handle, 1000, ";")) !== FALSE) {
        ?>
            <tr style="height: 20px;">
              <?php
              $num = count($data);
              $row++;
              $maxValue = 0.0;
              for ($c = 0; $c < $num; $c++) {
                if(floatval($data[$c])>$maxValue)
                  $maxValue = floatval($data[$c]);
              }
              ?>
              <td><?php echo $data[0]; ?></td>
              <?php                                                                                                
              for ($c = 1; $c < $num-1; $c++) {
              ?>
                <td style="background-color: <?php echo getColorCode(floatval($data[$c])/$maxValue) ?>;"><?php if (!$c)
                                                                                                  echo $data[$c]; ?></td>
              <?php
              }
              ?>
            </tr>
        <?php
          }
          fclose($handle);
        }
        ?>
      </tbody>
    </table>
  </body>

  </html>