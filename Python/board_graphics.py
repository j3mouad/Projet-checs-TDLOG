import chess
import chess.engine

board = chess.Board()
with chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish") as engine:
    result = engine.analyse(board, chess.engine.Limit(time=2.0))
    print("Evaluation:", result['score'])
    print(board)
