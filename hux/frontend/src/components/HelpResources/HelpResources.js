import { Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import React from 'react';
import CTImageCard from '../Cards/ImageCard/CTImageCard';

const HelpResources = withStyles(() => ({}))(({ classes, ...props }) => (
  <div className="helpResources">
    <Typography component="span" className="heading">
      {props.title}
    </Typography>
    <div className="helpCard-wrapper">
      {props.content &&
        props.content.length > 0 &&
        props.content.map((cnt) => (
          <CTImageCard
            key={cnt.id}
            maxWidth="289px"
            cardTitle={cnt.title}
            cardImage={cnt.image}
            cardDescription={cnt.description}
           />
        ))}
    </div>
  </div>
));
export default HelpResources;
