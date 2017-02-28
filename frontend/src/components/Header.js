import React, { Component } from 'react';

class Header extends Component {
    render() {
	return (
	    <header>
		<div className="container">
		    <div className="row">      
			<div className="col-xs-9 search">
			    <a className="logo">
				nexy
			    </a>
			</div>
		    </div>
		</div>
	    </header>
	)
    }
}

export default Header;
