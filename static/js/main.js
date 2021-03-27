let init = {
    fetchshows: function(){
        fetch('http://127.0.0.1:5000/api/most-rated/1',
        
        { method: 'get',
        credentials: 'same-origin',
        node: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(shows)
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(response){
            let shows = response.results
            let row = document.createElement('tr')
            let col1 = document.createElement('td')
            let col2 = document.createElement('td')
            let col3 = document.createElement('td')
            let col4 = document.createElement('td')
            let col5 = document.createElement('td')
            let col6 = document.createElement('td')
            let col7 = document.createElement('td')
            col1.innerHTML = shows.title;
            col2.innerHTML = response.year;
            col3.innerHTML = response.runtime;
            col4.innerHTML = response.trailer;
            col5.innerHTML = response.rating;
            col6.innerHTML = response.genres;
            col7.innerHTML = response.homepage
            row.appendChild(col1)
            row.appendChild(col2)
            row.appendChild(col3)
            row.appendChild(col4)
            row.appendChild(col5)
            row.appendChild(col6)
            row.appendChild(col7)
            document.querySelector('tbody').appendChild(row)
        })
    }
}





init.fetchshows()
