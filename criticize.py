from stockfish import Stockfish
import random
import chess

def criticizer(sf : Stockfish, move : str, b : chess.Board):
    if(sf.is_move_correct(move)):
        sf.make_moves_from_current_position([sf.get_best_move()]) # move to best position
        print(sf.get_board_visual())
        bestmoveCP = sf.get_evaluation().get('value')
        b.push(chess.Move.from_uci(move))
        sf.set_fen_position(b.board_fen())
        print(sf.get_board_visual())
        moveCP = sf.get_evaluation().get('value') # get your moves CP
        CPdiff = moveCP - bestmoveCP
        print(CPdiff)
        blunderPool = ['You ignorant cretin', 'My granddaughter plays better than you.', 'I am at a loss for words... and not in a good way']
        mistakePool = ["I really hope you don't have a future in chess", "That, ... was plain dumb", 'Good Tidings for the President of Losing']
        inaccuracyPool = ['That, ... was interesting', 'This match may be salvageable', 'Hikaru frowns upon you']
        complimentPool = ['Well Played', 'It looks like you know something about Chess at least', 'Good.', 'OK.' , 'Ehh.']
        insult = ''
        if(CPdiff <= -180):
            insult = random.choice(blunderPool)
            return insult
        if(-180 < CPdiff <= -50): 
            insult = random.choice(mistakePool)
            return insult
        if(-50 < CPdiff <= -10): 
            insult = random.choice(inaccuracyPool)
            return insult
        if(CPdiff == 0):
            insult = random.choice(['Impressive.', 'Masterful.', 'Beautiful'])
            return insult
        else: 
            insult = random.choice(complimentPool)
        return insult
    else:
        raise Exception('Invalid Chess Move')

