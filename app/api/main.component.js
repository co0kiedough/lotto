var MainApp = React.createClass({
    getInitialState: function(){
        return{
            currentMode: 'read',
            gameId: null
        };
    },
//    used when a click changes the mode.
//    currently only read all and read one.
    changeAppMode: function(newMode, gameId){
        this.setState({currentMode: newMode});
            if (gameId !== undefined){
                this.setState({gameId: gameId});
                //code
            }
    },
    
    render: function(){
        
        var modeComponent =
        <ReadGamesComponent
        changeAppMode={this.changeAppMode} />;
        
        switch(this.state.currentMode){
            case 'read':
                break;
            case 'readOne':
                modeComponent <ReadOneGameComponent gameId={this.state.gameId} changeAppMode={this.changeAppMode}/>;
                break;
        }
        
        return modeComponent;
    
    }
    
});
// render React component to 'content'
ReactDom.render(
    <MainApp />,
    document.getElementById('content')
);