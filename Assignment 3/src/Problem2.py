"""
    @author: Kinan Dak Al Bab
    @date:   26/10/2013
    
    This file computes the designated probabilities required by the Bayesian network created in the first question.
    it reads samples from a file "DataSet.txt" and calculates the value accordingly.

    The Variables in the network are:
        Basket_ball_on_tv :    abbreviated as B
        Geoge_watches_tv :     abbreviated as T
        out_of_dog_food :      abbreviated as F
        George_feeds_dog :     abbreviated as D
        
    The probabilities we need to Calculate:
        P(B)            requires counting +b (or -b) and counting the total number of samples.
        P(F)            requires counting +f (or -f) and counting the total number of samples.
        P(T | B)        requires counting (+t | +b), (+t | -b) and the number of samples containing +b (or -b) 
        P(D | F, T)     requires counting (+d | +f ^ +t), (+d | +f ^ -t), (+d | -f ^ +t), (+d | -f ^ -t). 
                            and the number of samples containing: (+f ^ +t), (+f ^ -t), (-f ^ +t), (-f ^ -t).

"""

if __name__ == '__main__':
    """main function:"""
    b_count = 0.0
    f_count = 0.0
    total = 0.0
    
    t_count_b = 0.0
    t_count_notb = 0.0
    
    d_count_f_t = 0.0
    d_count_f_nott = 0.0
    d_count_notf_t = 0.0
    d_count_notf_nott = 0.0
    
    total_f_t = 0.0
    total_f_nott = 0.0
    total_notf_t = 0.0
    total_notf_nott = 0.0
    
    with open("DataSet.txt") as f:  #open DataSet.txt
        for line in f:  #read each line
            line = line.strip() #trim string (remove tailing \n)
            var = []
            for i in range(0,4):    #reading the 4 elements on the line one after one and storing them in list
                var.append(line[0])
                line = line[1:].strip()
            
            total = total + 1
            if var[0] == "1":
                b_count = b_count + 1
            
            if var[2] == "1":
                f_count = f_count + 1
                
            if var[1] == "1" and var[0] == "1":
                t_count_b = t_count_b + 1
            elif var[1] == "1" and var[0] == "0":
                t_count_notb = t_count_notb + 1
                
            if var[2] == "1" and var[1] == "1":
                if var[3] == "1":
                    d_count_f_t = d_count_f_t + 1
                total_f_t = total_f_t + 1
            elif var[2] == "1" and var[1] == "0":
                if var[3] == "1":
                    d_count_f_nott = d_count_f_nott + 1
                total_f_nott = total_f_nott + 1
            elif var[2] == "0" and var[1] == "1":
                if var[3] == "1":
                    d_count_notf_t = d_count_notf_t + 1
                total_notf_t = total_notf_t + 1
            elif var[2] == "0" and var[1] == "0":
                if var[3] == "1":
                    d_count_notf_nott = d_count_notf_nott + 1
                total_notf_nott = total_notf_nott + 1
            
        notb_count = total - b_count
        
        t_b = t_count_b / b_count                           #p(+t|+b)
        nott_b = 1 - t_b                                    #p(-t|+b)
        t_notb = t_count_notb / notb_count                  #p(+t|-b)
        nott_notb = 1 - t_notb                              #p(-t|-b)
        
        b = b_count / total                                 #p(+b)
        notb = 1 - b                                        #p(-b)
        
        f = f_count / total                                 #p(+f)
        notf = 1 - f                                    #p(-f)
        
        d_f_t = d_count_f_t / total_f_t                     #p(+d|+f^+t)
        notd_f_t = 1 - d_f_t                                #p(-d|+f^+t)
        
        d_f_nott = d_count_f_nott / total_f_nott            #p(+d|+f^-t)
        notd_f_nott = 1 - d_f_nott                          #p(-d|+f^-t)
        
        d_notf_t = d_count_notf_t / total_notf_t            #p(+d|-f^+t)
        notd_notf_t = 1 - d_notf_t                          #p(-d|-f^+t)
        
        d_notf_nott = d_count_notf_nott / total_notf_nott   #p(+d|-f^-t)
        notd_notf_nott = 1 - d_notf_nott                    #p(-d|-f^-t)
        
        print "P(Basketball_on_tv):"
        print "\t p(+b)=", b
        print "\t p(-b)=", notb
        print ""
        print "P(George_watches_tv | Basketball_on_tv):"
        print "\t p(+t | +b)=", t_b
        print "\t p(-t | +b)=", nott_b
        print "\t p(+t | -b)=", t_notb
        print "\t p(-t | -b)=", nott_notb
        print ""
        print "P(Out_of_dog_food):"
        print "\t p(+f)=", f
        print "\t p(-f)=", notf
        print ""
        print "P(George_feeds_dog | Out_of_dog_food ^ George_watches_tv):"
        print "\t p(+d | +f ^ +t)=", d_f_t
        print "\t p(-d | +f ^ +t)=", notd_f_t
        print "\t p(+d | +f ^ -t)=", d_f_nott
        print "\t p(-d | +f ^ -t)=", notd_f_nott
        print "\t p(+d | -f ^ +t)=", d_notf_t
        print "\t p(-d | -f ^ +t)=", notd_notf_t
        print "\t p(+d | -f ^ -t)=", d_notf_nott
        print "\t p(-d | -f ^ -t)=", notd_notf_nott
        