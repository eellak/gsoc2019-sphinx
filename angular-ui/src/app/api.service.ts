import { Injectable, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';


@Injectable({
  providedIn: 'root'
})
export class ApiService implements OnInit {
  private cookieValue: string;

  constructor(private httpClient: HttpClient, private cookieService: CookieService) {
    this.cookieService.set('id', Math.random().toString())
    this.cookieValue = this.cookieService.get('id')
  }

  ngOnInit() {
  }

  getCookieService() {
    return this.cookieValue
  }
  public getUrlService() {
    let headers: HttpHeaders = new HttpHeaders();
    headers = headers.append('cookie', this.cookieValue);
    return this.httpClient.get("http://127.0.0.1:5000/login", { headers })
  }

  public getMessagesService() {
    return this.httpClient.get("http://127.0.0.1:5000/messages")
  }

  public getUserService() {
    return this.httpClient.get("http://127.0.0.1:5000/user")
  }

}
