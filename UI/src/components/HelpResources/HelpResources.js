import { Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import React from 'react';

const card =  ( ) 

const HelpResources = withStyles((theme) => ({
  },
)(({ classes, ...props }) => {
  return (
    <>
          <Typography component="h6">{props.title}</Typography>
          <div></div>
    </>
  );
});
export default HelpResources;
