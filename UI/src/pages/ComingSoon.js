import React from "react";
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  root: {
    height: '100vh',
display:'flex',
        minHeight: '100vh',
        alignItems: "center",
        flexDirection: "column",
        justifyContent: "center",
  },
  heading: {
    color: "#00C395",
      fontSize: 40,
    fontWeight: 800,
    marginBottom: 16,
  },
  subheading: {
    color: "#3E4246",
    fontSize: 14,
    maxWidth: 650,
    textAlign: "center",
  },
  label: {
    marginTop: theme.spacing(1),
  },
}));

const ComingSoon = () => {
    const classes = useStyles();
  return (
    <div className={classes.root}>
          <h2 className={classes.heading}>We are on the WAY!</h2>
          <strong>Stay tuned for something amazing</strong>
    </div>
  );
};

export default ComingSoon;
