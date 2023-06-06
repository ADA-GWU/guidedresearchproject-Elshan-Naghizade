CREATE TABLE Main_tab_
(
  Relative_Location_ VARCHAR(25000) NOT NULL,
  Height_ INT NOT NULL,
  Width_ INT NOT NULL,
  Channels_ INT NOT NULL,
  File_Type_ VARCHAR(25) NOT NULL,
  Image_id_ INT NOT NULL,
  PRIMARY KEY (Image_id_)
);

CREATE TABLE Array_Tab_
(
  Array_location_ VARCHAR(25000) NOT NULL,
  Array_type_ VARCHAR(100) NOT NULL,
  Image_id_ INT NOT NULL,
  PRIMARY KEY (Image_id_),
  FOREIGN KEY (Image_id_) REFERENCES Main_tab_(Image_id_)
);

CREATE TABLE Feature_Tab_
(
  Histogram_ VARCHAR(2500) NOT NULL,
  Edges_ VARCHAR(2500) NOT NULL,
  Corners_ VARCHAR(2500) NOT NULL,
  Image_id_ INT NOT NULL,
  PRIMARY KEY (Image_id_),
  FOREIGN KEY (Image_id_) REFERENCES Main_tab_(Image_id_)
);