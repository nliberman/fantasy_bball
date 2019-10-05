## Pulling file from NBA.com
open text editor like atom
Paste in the first line as follows:
PLAYER	TEAM	AGE	GP	W	L	MIN	PTS	FGM	FGA	FG%	3PM	3PA	3P%	FTM	FTA	FT%	OREB	DREB	REB	AST	TOV	STL	BLK	PF	FP	DD2	TD3	+/-

The following lines should be in the format below... line1: playername, line2: stats, line3: index number
1
Paul George
OKC	29	25	13	12	38.6	28.0	8.9	21.5	41.4	3.9	11.1	35.0	6.3	7.4	84.9	1.2	7.4	8.6	4.4	2.8	2.0	0.4	2.8	49.2	8	1	2.9
2
Russell Westbrook
OKC	30	28	15	13	36.9	25.5	9.4	21.3	44.3	2.5	7.5	33.0	4.1	6.1	67.8	1.6	9.5	11.1	10.1	4.3	1.5	0.6	3.3	56.0	21	14	0.5
3


## clean the txt file from nba.com
python3 clean_nba_dot_com_stats.py unclean_txt_file
example:
  python3 clean_nba_dot_com_stats.py stats19_post_break.txt


## run the valuing system... in the format of pro basketball reference
python3 main.py csv_to_analyze num_teams
example:
  python3 main.py stats19_post_break.csv 15
