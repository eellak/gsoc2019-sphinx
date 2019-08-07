import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { HttpHeaders, HttpParams } from '@angular/common/http';
import { UserService } from '../UserService'

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})

export class SignUpComponent implements OnInit {
  messages: any;

  constructor(private apiService: ApiService, private userService: UserService) {

  }

  ngOnInit() {
  }


  login() {
    this.userService.signIn()
  }

  getMessages() {
    let body = new HttpParams().set('token', UserService.SESSION_STORAGE_KEY);
    let headers: HttpHeaders = new HttpHeaders();
    headers = headers.append('Content-Type', 'application/x-www-form-urlencoded');
    this.apiService.getMessagesService(body, headers).subscribe((data) => {
      this.messages = data;
    })
  }

}
