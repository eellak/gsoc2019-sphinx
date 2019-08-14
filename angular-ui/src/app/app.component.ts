import { Component, OnInit } from '@angular/core';
import { ApiService } from './api.service';
import { MyCookieService } from './cookie.service'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'angular-ui';

  constructor(private cookieServ: MyCookieService) { }

  public ngOnInit(): void {
  }



}
