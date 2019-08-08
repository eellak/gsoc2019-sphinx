import { Injectable, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
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
  public getInfoService(body: HttpParams, headers: HttpHeaders) {
    return this.httpClient.post("http://127.0.0.1:5000/info", body, {
      headers
    })
  }
  public getMessagesService(body: HttpParams, headers: HttpHeaders) {
    return this.httpClient.post("http://127.0.0.1:5000/messages", body, {
      headers
    })
  }

}
