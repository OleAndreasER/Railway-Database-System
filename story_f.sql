/*
f) Det skal legges inn nødvendige data slik at systemet kan håndtere billettkjøp for de tre togrutene
på Nordlandsbanen, mandag 3. april og tirsdag 4. april i år. Dette kan gjøres med et skript, dere
trenger ikke å programmere støtte for denne funksjonaliteten..
*/

INSERT INTO TrainOccurence(trainOccurenceId, date, trainRouteId)
VALUES
    (1, "2023-04-03", 1),
    (2, "2023-04-03", 2),
    (3, "2023-04-03", 3),

    (4, "2023-04-04", 1),
    (5, "2023-04-04", 2),
    (6, "2023-04-04", 3);
