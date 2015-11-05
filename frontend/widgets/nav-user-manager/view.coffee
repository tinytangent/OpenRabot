User = require('../../models/user.coffee')
md5 = require('../../commons/logic/md5.coffee')

# a class to setup user manage interface on navbar
class NavUserManager

  AVATAR_BASE: "http://www.gravatar.com/avatar/"

  # Construct the navbar login / logout interface
  constructor: (topDom) ->
    @user = new User
    @user.on('update', @update.bind(@))
    @user.sync()

    $(topDom).find('.num-gv-login').click(@login.bind(@))
    $(topDom).find('.num-gv-logout').click(@user.logout.bind(@user))

    @guestView = $(topDom).find('.num-guest-view')
    @guestViewUsername = $(topDom).find('.num-gv-username')
    @guestViewPassword = $(topDom).find('.num-gv-password')
    @userView = $(topDom).find('.num-user-view')
    @userViewUsername = $(topDom).find('.num-uv-username')
    @userImg = $(topDom).find('.num-userinfo')

  login: ->
    username = @guestViewUsername.val()
    password = @guestViewPassword.val()
    @user.login username, password, (err) ->
      throw new Error(err)

  update: ->
    if @user.loggedin
      @userView.removeClass('hidden')
      @guestView.addClass('hidden')
      @userViewUsername.text(@user.user.username)
      userhash = md5(@user.user.email)
      @userImg.attr('src', "#{@AVATAR_BASE}#{userhash}?d=identicon")

    else
      @userView.addClass('hidden')
      @guestView.removeClass('hidden')
      @userImg.attr('src', "#{@AVATAR_BASE}nobody?d=mm")


module.exports = NavUserManager