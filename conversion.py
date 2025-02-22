def geodicToCartesian(geodic_list): #geodic list contains latitude, longitude, and altitude
  n_fi = a/(math.sqrt(1-E*(math.sin(geodic_list[0]))**2))
  x = (n_fi + geodic_list[2])*math.cos(geodic_list[0])*math.cos(geodic_list[1])
  y = (n_fi + geodic_list[2])*math.cos(geodic_list[0])*math.sin(geodic_list[1])
  z = ((1-E)*n_fi + geodic_list[2])*math.sin(geodic_list[0])
  return([x,y,z])
