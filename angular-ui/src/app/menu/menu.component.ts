import { Component, OnInit } from '@angular/core';
import { LogInComponent } from '../log-in/log-in.component'
import { MyCookieService } from '../cookie.service'
import { HttpHeaders, HttpParams } from '@angular/common/http';
import { ApiService } from '../api.service';

@Component({
  providers: [LogInComponent],
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {

  constructor(private apiService: ApiService, private signComp: LogInComponent, private cookieServ: MyCookieService) { }

  ngOnInit() {
  }

  getCookie() {
    return this.cookieServ.getCookie()
  }

  logOut() {
    let body = new HttpParams().set('cookie', this.getCookie());
    let headers: HttpHeaders = new HttpHeaders();
    headers = headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers = headers.append('Access-Control-Allow-Origin', '*');
    headers = headers.append("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    this.apiService.logOut(body, headers).subscribe((data) => {
      window.sessionStorage.clear();
      window.location.href = '/log-in';
    })

  }
}
