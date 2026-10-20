-- Contrôle dans WH_Bixi : trajets par jour, 14 lignes attendues après l'exécution 2
SELECT LEFT(CAST(started_at AS varchar(30)), 10) AS jour, COUNT(*) AS trajets FROM dbo.trips GROUP BY LEFT(CAST(started_at AS varchar(30)), 10) ORDER BY jour;
