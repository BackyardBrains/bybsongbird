import sox 
trans = sox.Transformer()
trans.trim(0,2)
trans.build('/home/anusha/Project/Test/goldfinch_test.wav','out.wav')


